from fastapi import APIRouter, HTTPException
from typing import List

from models import Product, ProductCreate, ProductRead, ProductUpdate
from database import Database


router = APIRouter(tags=["Products"], prefix="/products")

@router.get("/", response_model=List[ProductRead])
def get_products(db: Database, limit: int = 100, offset: int = 0):
    db_products = db.query(Product).offset(offset).limit(limit).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="No products found")
    return db_products

@router.get("/{product_id}", response_model=ProductRead)
def get_product(db: Database, product_id: int):
    db_product = db.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", status_code=201, response_model=ProductRead)
def add_product(db: Database, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(db: Database, product_id: int, product: ProductUpdate):
    db_product = db.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", response_model=ProductRead)
def delete_product(db: Database, product_id: int):
    db_product = db.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product