from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)
from app.services.embedding_service import create_embedding
from app.core.security import require_admin, get_current_user
from app.models.user import User
from app.services.sale_service import create_sale

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)



@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    text = f"{product.name} {product.description}"

    embedding = create_embedding(text)

    new_product = Product(
        name=product.name,
        description=product.description,
        category=product.category,
        color=product.color,
        season=product.season,
        size=product.size,
        price=product.price,
        stock=product.stock,
        embedding=embedding
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product



@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()
    return products



@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    return product



@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    db_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not db_product:
        return {"message": "Product not found"}

    db_product.name = product.name
    db_product.description = product.description
    db_product.category = product.category
    db_product.color = product.color
    db_product.season = product.season
    db_product.size = product.size
    db_product.price = product.price
    db_product.stock = product.stock

    db.commit()
    db.refresh(db_product)

    return db_product



@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return {"message": "Product not found"}

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted",
        "id": product_id
    }

@router.patch("/{product_id}/stock")
def update_stock(
    product_id: int,
    action: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return {"message": "Product not found"}

    if action == "increase":
        product.stock += 1

    elif action == "decrease":
        product.stock -= 1

    if product.stock <= 0:
        db.delete(product)
        db.commit()

        return {
            "message": "Product deleted because stock reached 0"
        }

    db.commit()
    db.refresh(product)

    return {
        "id": product.id,
        "name": product.name,
        "stock": product.stock
    }

@router.post("/{product_id}/buy")
def buy_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return {"message": "Product not found"}

    if product.stock <= 0:
        return {"message": "Out of stock"}

    create_sale(
        user_id=current_user["user_id"],
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
        "message": "Purchase successful",
        "product": product.name
    }