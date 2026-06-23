from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func

from app.db.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    product_id = Column(Integer)

    quantity = Column(Integer, default=1)

    total_price = Column(Numeric(10, 2))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )