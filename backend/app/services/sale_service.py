from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.product import Product


def create_sale(
    user_id: int,
    product: Product,
    db: Session
):
    sale = Sale(
        user_id=user_id,
        product_id=product.id,
        quantity=1,
        total_price=product.price
    )

    db.add(sale)
    db.commit()

    return sale