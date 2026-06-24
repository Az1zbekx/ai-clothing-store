from sqlalchemy import text, and_, or_
from sqlalchemy.orm import Session
import re

from app.services.embedding_service import create_embedding
from app.models.product import Product


# ─── KATEGORIYA ──────────────────────────────────────────────
CATEGORY_KEYWORDS = {
    "bosh kiyim": ["cap", "hat", "shapka"],
    "shapka":     ["cap", "hat", "shapka"],
    "qalpoq":     ["cap", "hat"],
    "kepka":      ["cap", "hat"],
    "cap":        ["cap", "hat"],
    "hat":        ["cap", "hat"],

    "shim":       ["shim", "jins", "chino", "cargo", "jogger"],
    "jins":       ["jins", "shim"],
    "chino":      ["chino", "shim"],
    "cargo":      ["cargo", "shim"],

    # Apostrof bor/yo'q ikkala variant
    "ko'ylak":    ["ko'ylak", "shirt"],
    "koylak":     ["ko'ylak", "shirt"],   # apostrof yo'q
    "ko`ylak":    ["ko'ylak", "shirt"],   # backtick
    "shirt":      ["ko'ylak", "shirt"],

    "futbolka":   ["futbolka", "t-shirt", "polo"],
    "tshirt":     ["futbolka", "t-shirt"],
    "t-shirt":    ["futbolka", "t-shirt"],
    "polo":       ["polo", "futbolka"],

    "kofta":      ["kofta", "hoodie", "sweatshirt", "cardigan", "turtleneck", "angora", "zip"],
    "hoodie":     ["hoodie", "kofta"],
    "cardigan":   ["cardigan", "kofta"],
    "turtleneck": ["turtleneck", "kofta"],
    "angora":     ["angora", "kofta"],
    "sweatshirt": ["sweatshirt", "kofta"],

    "jaket":      ["jaket", "jacket", "blazer", "bomber", "puffer"],
    "jacket":     ["jaket", "jacket"],
    "blazer":     ["blazer", "jaket"],
    "bomber":     ["bomber", "jaket"],
    "puffer":     ["puffer", "jaket"],
}

# ─── RANG ─────────────────────────────────────────────────────
COLOR_KEYWORDS = {
    "qizil":     ["qizil", "red"],
    "ko'k":      ["ko'k", "blue"],
    "kok":       ["ko'k", "blue"],   # apostrof yo'q
    "oq":        ["oq", "white"],
    "qora":      ["qora", "black"],
    "yashil":    ["yashil", "green"],
    "sariq":     ["sariq", "yellow"],
    "kulrang":   ["kulrang", "grey", "gray"],
    "pushti":    ["pushti", "pink"],
    "binafsha":  ["binafsha", "purple"],
    "jigarrang": ["jigarrang", "brown"],
    "moviy":     ["moviy"],
    "zangori":   ["zangori"],
    "limon":     ["limon"],
    "tuproq":    ["tuproq"],
    "red":       ["qizil", "red"],
    "blue":      ["ko'k", "blue"],
    "black":     ["qora", "black"],
    "white":     ["oq", "white"],
    "green":     ["yashil", "green"],
    "yellow":    ["sariq", "yellow"],
    "grey":      ["kulrang", "grey"],
    "gray":      ["kulrang", "gray"],
    "pink":      ["pushti", "pink"],
}

# ─── MAVSUM ───────────────────────────────────────────────────
SEASON_KEYWORDS = {
    "yoz":    ["yoz", "summer"],
    "yozgi":  ["yoz", "summer"],
    "qish":   ["qish", "winter"],
    "qishki": ["qish", "winter"],
    "bahor":  ["bahor", "spring"],
    "kuz":    ["kuz", "autumn"],
    "summer": ["yoz", "summer"],
    "winter": ["qish", "winter"],
    "spring": ["bahor", "spring"],
    "autumn": ["kuz", "autumn"],
}

# ─── O'LCHAM ──────────────────────────────────────────────────
SIZE_KEYWORDS = {
    r'\bxs\b':                 ["XS"],
    r'\bs\b':                  ["S"],
    r'\bm\b':                  ["M"],
    r'\bl\b':                  ["L"],
    r'\bxl\b':                 ["XL"],
    r'\bxxl\b':                ["XXL"],
    r'kichik':                 ["XS", "S"],
    r'o[\'`]rta':              ["M"],
    r'orta':                   ["M"],
    r'katta':                  ["L", "XL"],
    r'juda\s*katta':           ["XXL"],
}


def normalize(text: str) -> str:
    """So'rovni normallashtiradi: kichik harf, apostrof variantlarni birlashtiradi"""
    text = text.lower()
    # Turli apostrof turlarini standartlashtirish
    text = text.replace("\u2019", "'").replace("`", "'").replace("\u02bc", "'")
    return text


def extract_filters(query: str) -> dict:
    """So'rovdan kategoriya, rang, mavsum va o'lcham filterlarini topadi"""
    q = normalize(query)

    filters = {
        "categories": [],
        "colors":     [],
        "seasons":    [],
        "sizes":      [],
    }

    for kw, vals in CATEGORY_KEYWORDS.items():
        if kw in q:
            filters["categories"].extend(vals)

    for kw, vals in COLOR_KEYWORDS.items():
        if kw in q:
            filters["colors"].extend(vals)

    for kw, vals in SEASON_KEYWORDS.items():
        if kw in q:
            filters["seasons"].extend(vals)

    for pattern, vals in SIZE_KEYWORDS.items():
        if re.search(pattern, q):
            filters["sizes"].extend(vals)

    # Takrorlarni olib tashlash
    filters["categories"] = list(set(filters["categories"]))
    filters["colors"]     = list(set(filters["colors"]))
    filters["seasons"]    = list(set(filters["seasons"]))
    filters["sizes"]      = list(set(filters["sizes"]))

    return filters


def build_keyword_query(db: Session, filters: dict):
    """Keyword filter bo'yicha qidiruv (kategoriya AND rang AND mavsum AND o'lcham)"""
    query = db.query(Product).filter(Product.stock > 0)
    conditions = []

    if filters["categories"]:
        conditions.append(or_(*[
            Product.category.ilike(f"%{cat}%")
            for cat in filters["categories"]
        ]))

    if filters["colors"]:
        conditions.append(or_(*[
            or_(
                Product.color.ilike(f"%{color}%"),
                Product.name.ilike(f"%{color}%"),
            )
            for color in filters["colors"]
        ]))

    if filters["seasons"]:
        conditions.append(or_(*[
            Product.season.ilike(f"%{season}%")
            for season in filters["seasons"]
        ]))

    if filters["sizes"]:
        conditions.append(or_(*[
            Product.size.ilike(f"%{size}%")
            for size in filters["sizes"]
        ]))

    if not conditions:
        return []

    return query.filter(and_(*conditions)).limit(6).all()


def search_products(query: str, db: Session):
    """
    Hybrid search:
    1. Keyword matching — kategoriya + rang + mavsum + o'lcham (AND mantiq)
    2. Vector search — fallback sifatida
    """
    filters = extract_filters(query)
    keyword_results = build_keyword_query(db, filters)

    # Vector search (har doim ishlaydi)
    query_embedding = create_embedding(query)
    sql = text("""
        SELECT id, name, description, category, color, season, size, price, stock
        FROM products
        WHERE stock > 0
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT 6
    """)
    vector_rows = db.execute(sql, {"embedding": str(query_embedding)}).fetchall()

    # Keyword natijalar birinchi, keyin vector (takror bo'lmagan)
    seen_ids = set()
    final_results = []

    for product in keyword_results:
        if product.id not in seen_ids:
            seen_ids.add(product.id)
            final_results.append(product)

    for row in vector_rows:
        if row.id not in seen_ids:
            seen_ids.add(row.id)
            class _P:
                pass
            p = _P()
            p.id          = row.id
            p.name        = row.name
            p.description = row.description
            p.category    = row.category
            p.color       = row.color
            p.season      = row.season
            p.size        = row.size
            p.price       = row.price
            p.stock       = row.stock
            final_results.append(p)

    return final_results[:6]