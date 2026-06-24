import re
import json
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, get_db, Base

from app.models.product import Product
from app.models.user import User
from app.models.sale import Sale
from app.models.chat_history import ChatHistory
from app.models.product import Product


from app.api.products import router as product_router
from app.api.auth import router as auth_router
from app.api.sales import router as sales_router
from app.api.boss import router as boss_router

from app.schemas.chat import ChatRequest, ChatResponse

from app.services.ai_service import ask_ai
from app.services.ai_chat_service import ask_general_chat
from app.services.vector_search_service import search_products, extract_filters
from app.services.chat_history_service import save_chat
from app.services.chat_history_service import get_last_chat
from app.services.sale_service import create_sale

from app.core.security import get_current_user




app = FastAPI(
    title="AI Clothing Store"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(auth_router)
app.include_router(boss_router)
app.include_router(sales_router)


@app.get("/")
def home():
    return {
        "message": "AI Clothing Store API"
    }


@app.get("/db-test")
def db_test():
    try:
        conn = engine.connect()
        conn.close()

        return {
            "status": "success",
            "message": "Database connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/chat", response_model=ChatResponse)
def chat_with_ai(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["user_id"]

    # Matn orqali xarid so'zlari ("ha"/"xa" olib tashlandi — juda keng ushlab turar edi)
    purchase_words = [
        "olaman",
        "sotib olaman",
        "olib ber",
        "maqul",
        "olmoqchiman",
        "xarid qilaman",
        "buyurtma beraman"
    ]

    pattern = r'\b(' + '|'.join(re.escape(w) for w in purchase_words) + r')\b'
    if re.search(pattern, data.message.lower()):

        last_chat = get_last_chat(
            user_id=user_id,
            db=db
        )

        if not last_chat or not last_chat.product_id:
            return {
                "response": "❗ Avval qaysi mahsulotni xohlayotganingizni ayting, men topib beraman!"
            }

        product = db.query(Product).filter(
            Product.id == last_chat.product_id
        ).first()

        if not product:
            return {
                "response": "❗ Kechirasiz, bu mahsulot endi mavjud emas. Boshqasini tanlang."
            }

        if product.stock <= 0:
            return {
                "response": f"❗ Afsuski, {product.name} tugab ketgan. Boshqa mahsulot tanlang."
            }

        create_sale(
            user_id=user_id,
            product=product,
            db=db
        )

        product.stock -= 1

        if product.stock <= 0:
            db.delete(product)
        else:
            db.add(product)

        db.commit()

        return {
            "response": f"✅ **{product.name}** muvaffaqiyatli sotib olindi! Yaxshi xarid! 🎉"
        }

    # Qidiruv yoki oddiy suhbat ekanligini aniqlaymiz
    filters = extract_filters(data.message)
    
    # Kategoriya, rang, mavsum, o'lcham kabi parametrlar bormi? Yoki kiyimga oid kalit so'zlar
    msg_words = re.findall(r'\b\w+\b', data.message.lower())
    product_keywords = {"kiyim", "narsa", "bor", "kerak", "qanaqa", "ko'rsat", "top", "ber"}
    
    is_product_query = any(filters.values()) or bool(set(msg_words) & product_keywords)

    if not is_product_query:
        answer = ask_general_chat(data.message)
        save_chat(
            user_id=user_id,
            user_message=data.message,
            ai_response=answer,
            product_id=None,
            db=db
        )
        return {
            "response": answer,
            "recommended_products": None
        }

    products = search_products(
        data.message,
        db
    )

    # Top 3 mahsulot AI uchun matn
    products_text = ""
    for p in products[:3]:
        products_text += f"- {p.name} ({p.category}, {p.color}, {p.size}, {p.price} so'm)\n"

    answer = ask_ai(
        data.message,
        products_text
    )

    # 1-mahsulot IDsi saqlanadi — matn orqali "olaman" deganda shu sotiladi
    # To'g'ri xarid esa har bir kartaning tugmasi orqali /products/{id}/buy
    save_chat(
        user_id=user_id,
        user_message=data.message,
        ai_response=answer,
        product_id=products[0].id if products else None,
        db=db
    )

    recommended = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "season": p.season,
            "color": p.color,
            "size": p.size,
            "price": float(p.price)
        }
        for p in products[:3]
    ]

    return {
        "response": answer,
        "recommended_products": recommended if recommended else None
    }

@app.get("/me")
def me(
    current_user=Depends(get_current_user)
):
    return current_user