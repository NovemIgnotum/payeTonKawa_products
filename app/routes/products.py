from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.products import Product as ProductBase, ProductCreate, ProductUpdate, ProductResponse as Response, getResponse
from model.products import Product as DBProduct
from datetime import datetime, timezone

router = APIRouter()

@router.post("/products", response_model=Response, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        if not product.name or product.price is None or product.stock_quantity is None:
            return JSONResponse(status_code=400, content={"message": "Name, price, and stock quantity are required."})
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
       
@router.get("/products/{product_id}", response_model=Response, status_code=200)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "message": "Product retrieved successfully.",
        "product": ProductBase.model_validate(product)
    }

@router.get("/products", response_model=getResponse, status_code=200)
def get_products(db: Session = Depends(get_db)):
    products = db.query(DBProduct).all()
    print(f"Retrieved {len(products)} products from the database.")
    return {
        "message": "All products retrieved successfully.",
        "product": [ProductBase.model_validate(product) for product in products]
    }

    
@router.put("/products/{product_id}", response_model=Response, status_code=200)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product_in_db = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product_in_db:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product_in_db, key, value)
    db.commit()
    db.refresh(product_in_db)
    return {
        "message": "Product updated successfully.",
        "product": ProductBase.model_validate(product_in_db)
    }

@router.delete("/products/{product_id}", response_model=Response, status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {
        "message": "Product deleted successfully.",
        "product": ProductBase.model_validate(product)
    }