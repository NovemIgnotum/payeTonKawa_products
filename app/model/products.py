from sqlalchemy import Column, Float, VARCHAR, TIMESTAMP, Integer
from database.session import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(127), nullable=False)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    
    class Config:
        from_attributes__ = True