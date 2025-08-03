from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float
    stock_quantity: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class ProductInDB(ProductBase):
    id: int

    

    class Config:
        from_attributes = True

class Product(ProductInDB):
    pass


class ProductResponse(BaseModel):
    message: str
    product: ProductInDB

    class Config:
        from_attributes = True
        
class getResponse(BaseModel):
    message: str
    product: list[ProductInDB]

    class Config:
        from_attributes = True