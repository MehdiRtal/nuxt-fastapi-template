from fastapi import APIRouter, HTTPException
from typing import List

from models import *
from database import DBSession


router = APIRouter(tags=["Products"], prefix="/products")

@router.get("/", response_model=List[ProductRead])
def get_products(db_session: DBSession, limit: int = 100, offset: int = 0):
    db_products = db_session.query(Product).offset(offset).limit(limit).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="No products found")
    return db_products

@router.get("/{product_id}", response_model=ProductRead)
def get_product(db_session: DBSession, product_id: int):
    db_product = db_session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", status_code=201, response_model=ProductRead)
def create_product(db_session: DBSession, product: ProductCreate):
    db_product = Product(**product.dict())
    db_session.add(db_product)
    db_session.commit()
    db_session.refresh(db_product)
    return db_product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(db_session: DBSession, product_id: int, product: ProductUpdate):
    db_product = db_session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db_session.add(db_product)
    db_session.commit()
    db_session.refresh(db_product)
    return db_product

@router.delete("/{product_id}", response_model=ProductRead)
def delete_product(db_session: DBSession, product_id: int):
    db_product = db_session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_session.delete(db_product)
    db_session.commit()
    return db_product