from fastapi import FastAPI
from app.db.database import engine
from app.api.products import router as product_router
from app.models import Product
from app.services.ai_service import ask_ai
from app.schemas.chat import ChatRequest, ChatResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db
from app.services.product_service import get_all_products


app = FastAPI(
    title="AI Clothing Store"
)



app.include_router(product_router)



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

    products = get_all_products(db)

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

    answer = ask_ai(data.message, products_text)

    return {
        "response": answer
    }
