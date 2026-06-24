"""
AI Service — kichik model (qwen2.5:1.5b) o'zbek tilini to'liq bilmaydi.
Shuning uchun statik, sinovdan o'tgan shablonlardan foydalanamiz.
Model faqat kelajakda katta model qo'shilganda ishlatiladi.
"""

# ============================================================
# STATIK SHABLONLAR — har doim to'g'ri, har doim o'zbek tilida
# ============================================================

CATEGORY_TEMPLATES = {
    "bosh kiyim": "Sizga mos bosh kiyimlar topildi! 🧢",
    "shapka": "Sizga mos shapkalar topildi! 🧢",
    "kepka": "Zo'r kepkalar mana! 🧢",
    "cap": "Zo'r kepkalar mana! 🧢",
    "hat": "Bosh kiyimlar topildi! 🧢",
    "shim": "Sizga mos shimlar topildi! 👖",
    "jins": "Zamonaviy jinslar mana! 👖",
    "chino": "Chiroyli chinolar topildi! 👖",
    "cargo": "Qulay cargo shimlar mana! 👖",
    "jogger": "Sport jogger shimlar topildi! 👖",
    "ko'ylak": "Chiroyli ko'ylaklar topildi! 👗",
    "koylak":  "Chiroyli ko'ylaklar topildi! 👗",   # apostrof yo'q
    "ko`ylak": "Chiroyli ko'ylaklar topildi! 👗",   # backtick
    "shirt": "Chiroyli ko'ylaklar topildi! 👗",
    "futbolka": "Sizga mos futbolkalar! 👕",
    "t-shirt": "Sizga mos futbolkalar! 👕",
    "polo": "Klassik polo futbolkalar mana! 👕",
    "kofta": "Iliq va chiroyli koftalar mana! 🧥",
    "hoodie": "Qulay hoodie va koftalar! 🧥",
    "cardigan": "Yumshoq cardiganlar topildi! 🧥",
    "turtleneck": "Issiq turtlenecklar mana! 🧥",
    "angora": "Yumshoq angora koftalar topildi! 🧥",
    "sweatshirt": "Qulay sweatshirtlar mana! 🧥",
    "jaket": "Zamonaviy jaketlar topildi! 🧥",
    "jacket": "Zamonaviy jaketlar topildi! 🧥",
    "blazer": "Elegant blazerlar mana! 🧥",
    "bomber": "Zo'r bomberlar topildi! 🧥",
    "puffer": "Issiq puffer jaketlar mana! 🧥",
    "yozgi": "Yozlik engil kiyimlar mana! ☀️",
    "yoz": "Yoz uchun zo'r tanlovlar! ☀️",
    "summer": "Yozlik kiyimlar topildi! ☀️",
    "qishki": "Qishlik iliq kiyimlar topildi! ❄️",
    "qish": "Qish uchun iliq variantlar! ❄️",
    "winter": "Qishlik issiq kiyimlar mana! ❄️",
    "bahor": "Bahorlik yangi kiyimlar! 🌸",
    "kuz": "Kuzlik kiyimlar topildi! 🍂",
    "qizil": "Qizil rangdagi kiyimlar topildi! ❤️",
    "red": "Qizil rangdagi kiyimlar topildi! ❤️",
    "ko'k": "Ko'k rangdagi kiyimlar mana! 💙",
    "blue": "Ko'k rangdagi kiyimlar mana! 💙",
    "oq": "Oq rangdagi kiyimlar topildi! 🤍",
    "white": "Oq rangdagi kiyimlar topildi! 🤍",
    "qora": "Qora rangdagi kiyimlar mana! 🖤",
    "black": "Qora rangdagi kiyimlar mana! 🖤",
    "yashil": "Yashil rangdagi kiyimlar! 💚",
    "green": "Yashil rangdagi kiyimlar! 💚",
    "sariq": "Sariq rangdagi kiyimlar topildi! 💛",
    "yellow": "Sariq rangdagi kiyimlar topildi! 💛",
    "kulrang": "Kulrang kiyimlar mana! 🩶",
    "grey": "Kulrang kiyimlar mana! 🩶",
    "pushti": "Pushti kiyimlar topildi! 🩷",
    "pink": "Pushti kiyimlar topildi! 🩷",
    "jigarrang": "Jigarrang kiyimlar mana! 🤎",
    "brown": "Jigarrang kiyimlar mana! 🤎",
    "moviy": "Moviy rangdagi kiyimlar! 💙",
    "binafsha": "Binafsha rangdagi kiyimlar! 💜",
    "zangori": "Zangori rangdagi kiyimlar topildi!",
    "limon": "Limon rangdagi kiyimlar mana! 💛",
    "tuproq": "Tuproq rangdagi kiyimlar topildi!",
    "issiq": "Iliq va qulay kiyimlar topildi! 🔥",
    "sport": "Sport kiyimlar mana! 💪",
    "zamonaviy": "Zamonaviy uslubdagi kiyimlar! ✨",
    "arzon": "Byudjetingizga mos kiyimlar topildi! 💰",
    "slim": "Slim fit kiyimlar topildi! ✨",
    "oversize": "Oversize kiyimlar mana! 😎",
    "linen": "Engil linen kiyimlar topildi! 🌿",
    "denim": "Klassik denim kiyimlar mana! 👖",
    # O'lchamlar
    " s ": "S o'lchamdagi kiyimlar topildi! 👕",
    " m ": "M o'lchamdagi kiyimlar topildi! 👕",
    " l ": "L o'lchamdagi kiyimlar topildi! 👕",
    "xl":  "XL o'lchamdagi kiyimlar topildi! 👕",
    "xxl": "XXL o'lchamdagi kiyimlar topildi! 👕",
    "kichik": "Kichik o'lchamdagi kiyimlar topildi! 👕",
    "o'rta":  "O'rta o'lchamdagi kiyimlar topildi! 👕",
    "orta":   "O'rta o'lchamdagi kiyimlar topildi! 👕",
    "katta":  "Katta o'lchamdagi kiyimlar topildi! 👕",
}

DEFAULT_FOUND = "Mana sizga mos mahsulotlar topildi! 😊"
DEFAULT_NOT_FOUND = "Afsuski, so'ragan mahsulotingizni topolmadim. 😔 Boshqa kiyim turi yoki rang ko'rib ko'ring!"


import re as _re

def ask_ai(message: str, products_text: str) -> str:
    """
    Ishonchli, tez va har doim to'g'ri o'zbek tilida javob beradi.
    """
    has_products = bool(products_text.strip())

    if not has_products:
        return DEFAULT_NOT_FOUND

    # Normalizatsiya: apostrof variantlarini birlashtirish
    msg_lower = message.lower()
    msg_lower = msg_lower.replace("\u2019", "'").replace("`", "'").replace("\u02bc", "'")
    # Bo'sh joy qo'shib S/M/L uchun to'g'ri matching
    msg_padded = f" {msg_lower} "

    # O'lcham regex tekshiruvi (birinchi — aniqroq)
    size_patterns = {
        r'\bxxl\b': "XXL o'lchamdagi kiyimlar topildi! 👕",
        r'\bxl\b':  "XL o'lchamdagi kiyimlar topildi! 👕",
        r'\bl\b':   "L o'lchamdagi kiyimlar topildi! 👕",
        r'\bm\b':   "M o'lchamdagi kiyimlar topildi! 👕",
        r'\bs\b':   "S o'lchamdagi kiyimlar topildi! 👕",
        r'\bxs\b':  "XS o'lchamdagi kiyimlar topildi! 👕",
    }
    for pattern, tmpl in size_patterns.items():
        if _re.search(pattern, msg_lower):
            return tmpl

    # Kalit so'z bo'yicha shablon
    for keyword, template in CATEGORY_TEMPLATES.items():
        if keyword in msg_padded:
            return template
    # Aniq substring (apostrof bor/yo'q variant)
    for keyword, template in CATEGORY_TEMPLATES.items():
        if keyword in msg_lower:
            return template

    return DEFAULT_FOUND