from sqlalchemy import Column, Integer, String, Text, Numeric
from app.db.database import Base
from pgvector.sqlalchemy import Vector

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    color = Column(String(50))
    season = Column(String(50))
    size = Column(String(50))
    price = Column(Numeric(10, 2))
    stock = Column(Integer, default=0)

    embedding = Column(Vector(768))