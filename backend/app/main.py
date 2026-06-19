from fastapi import FastAPI
from app.db.database import engine
from app.api.products import router as product_router
from app.models import Product

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