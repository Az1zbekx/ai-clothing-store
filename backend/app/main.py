from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.database import engine, get_db, Base

from app.models.product import Product
from app.models.user import User
from app.models.sale import Sale
from app.models.chat_history import ChatHistory
from app.models.product import Product


from app.api.products import router as product_router
from app.api.auth import router as auth_router

from app.schemas.chat import ChatRequest, ChatResponse

from app.services.ai_service import ask_ai
from app.services.vector_search_service import search_products
from app.services.chat_history_service import save_chat
from app.services.chat_history_service import get_last_chat
from app.services.sale_service import create_sale

from fastapi.middleware.cors import CORSMiddleware

from app.core.security import get_current_user
from app.services.sale_service import create_sale



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
    db: Session = Depends(get_db)
):

    purchase_words = [
        "olaman",
        "ha",
        "sotib olaman",
        "olib ber"
    ]

    if data.message.lower() in purchase_words:

        last_chat = get_last_chat(
            user_id=1,
            db=db
        )

        if not last_chat:
            return {
                "response": "Oldin mahsulot tanlang"
            }

        if not last_chat.product_id:
            return {
                "response": "Mahsulot topilmadi"
            }

        product = db.query(Product).filter(
            Product.id == last_chat.product_id
        ).first()

        if not product:
            return {
                "response": "Mahsulot mavjud emas"
            }

        create_sale(
            user_id=1,
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
            "response": f"{product.name} muvaffaqiyatli sotib olindi"
        }

    products = search_products(
        data.message,
        db
    )

    products_text = ""

    for p in products:
        products_text += f"""
Name: {p.name}
Description: {p.description}
Category: {p.category}
Color: {p.color}
Season: {p.season}
Size: {p.size}
Price: {p.price}
Stock: {p.stock}

"""

    answer = ask_ai(
        data.message,
        products_text
    )

    save_chat(
        user_id=1,
        user_message=data.message,
        ai_response=answer,
        product_id=products[0].id if products else None,
        db=db
    )

    return {
        "response": answer
    }

@app.get("/me")
def me(
    current_user=Depends(get_current_user)
):
    return current_user