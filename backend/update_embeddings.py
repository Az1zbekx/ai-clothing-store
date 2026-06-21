from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.product import Product
from app.services.embedding_service import create_embedding

db: Session = SessionLocal()

products = db.query(Product).all()

for product in products:

    text = f"""
    {product.name}
    {product.description}
    {product.category}
    {product.color}
    {product.season}
    {product.size}
    """

    product.embedding = create_embedding(text)

    print(f"Updated: {product.name}")

db.commit()
db.close()

print("Done")