from fastapi import FastAPI
from app.db.database import engine

app = FastAPI(
    title="AI Clothing Store"
)

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