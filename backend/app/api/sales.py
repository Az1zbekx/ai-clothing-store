from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.sale import Sale
from app.models.product import Product
from app.core.security import get_current_user

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

@router.get("/my-history")
def my_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    sales = (
        db.query(Sale)
        .filter(
            Sale.user_id == current_user["user_id"]
        )
        .all()
    )

    result = []

    for sale in sales:

        product = (
            db.query(Product)
            .filter(
                Product.id == sale.product_id
            )
            .first()
        )

        result.append({
            "sale_id": sale.id,
            "product": product.name if product else "Deleted Product",
            "quantity": sale.quantity,
            "total_price": float(sale.total_price),
            "created_at": sale.created_at
        })

    return result