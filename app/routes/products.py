from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.products import Product as ProductBase, ProductCreate, ProductUpdate, ProductResponse as Response
from model.products import Product as DBProduct
from datetime import datetime, timezone

router = APIRouter()

@router.post("/products", response_model=Response, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        existing_product = db.query(DBProduct).filter(DBProduct.name == product.name).first()
        if existing_product:
            return JSONResponse(status_code=400, content={"message": "Product with this name already exists."})
        # Add a timestamp for creation as ISO string
        now_iso = datetime.now(timezone.utc).isoformat()
        product.created_at = now_iso
        product.updated_at = now_iso
        new_product = DBProduct(**product.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {
            "message": "Product created successfully.",
            "product": ProductBase.model_validate(new_product)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/products/{product_id}", response_model=Response)
def get_product(product_id: int, db: Session = Depends(get_db)):
    pass

