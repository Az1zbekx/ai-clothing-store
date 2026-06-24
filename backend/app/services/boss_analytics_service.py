from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.sale import Sale
from app.models.product import Product


def get_total_revenue(db: Session):

    revenue = (
        db.query(
            func.sum(Sale.total_price)
        ).scalar()
        or 0
    )

    return float(revenue)


def get_total_sales(db: Session):

    return db.query(Sale).count()



def get_top_products(db: Session):

    result = (
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
        .all()
    )

    return result


def get_low_stock_products(db: Session):

    products = (
        db.query(Product)
        .filter(Product.stock <= 5)
        .all()
    )

    return products

def get_recent_sales(db: Session):

    sales = (
        db.query(Sale)
        .order_by(Sale.created_at.desc())
        .limit(10)
        .all()
    )

    return sales