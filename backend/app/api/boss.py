from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db

from app.models.user import User
from app.models.product import Product
from app.models.sale import Sale

from app.core.security import require_boss

from app.schemas.chat import ChatRequest

from app.services.boss_ai_service import (
    ask_boss_ai,
    build_analytics_context
)

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


@router.get("/analytics")
def analytics(
    db: Session = Depends(get_db),
    current_user=Depends(require_boss)
):
    total_sales = db.query(Sale).count()

    total_revenue = (
        db.query(func.sum(Sale.total_price))
        .scalar()
        or 0
    )

    top_product = (
        db.query(
            Product.name,
            func.count(Sale.id).label("sales_count")
        )
        .join(
            Sale,
            Product.id == Sale.product_id
        )
        .group_by(Product.id)
        .order_by(
            func.count(Sale.id).desc()
        )
        .first()
    )

    low_stock = (
        db.query(Product)
        .filter(Product.stock <= 5)
        .all()
    )

    return {
        "total_sales": total_sales,
        "total_revenue": float(total_revenue),
        "top_product": top_product[0] if top_product else None,
        "low_stock": [p.name for p in low_stock]
    }


@router.post("/ai")
def boss_ai(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_boss)
):

    analytics_text = build_analytics_context(db)

    answer = ask_boss_ai(
        data.message,
        analytics_text
    )

    return {
        "response": answer
    }

