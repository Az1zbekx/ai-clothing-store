from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.sale import Sale

from app.core.security import require_boss

router = APIRouter(
    prefix="/boss",
    tags=["Boss"]
)

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_boss)
):
    total_users = db.query(User).count()

    total_products = db.query(Product).count()

    total_sales = db.query(Sale).count()

    total_revenue = (
        db.query(
            func.sum(Sale.total_price)
        ).scalar()
        or 0
    )

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_sales": total_sales,
        "total_revenue": float(total_revenue)
    }