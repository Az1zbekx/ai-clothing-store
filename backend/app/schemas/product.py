from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    category: str
    color: str
    season: str
    size: str
    price: float
    stock: int


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True

class ProductUpdate(ProductCreate):
    pass