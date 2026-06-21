from app.db.database import SessionLocal
from app.services.vector_search_service import search_products

db = SessionLocal()

results = search_products(
    "Menga yozgi oq futbolka kerak",
    db
)

for item in results:
    print(item.name)

db.close()