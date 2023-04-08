from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models import *
from database import Session, get_session


router = APIRouter(tags=["Products"], prefix="/products")

@router.get("/", response_model=List[ProductRead])
def get_products(limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    db_products = session.query(Product).offset(offset).limit(limit).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="No products found")
    return db_products

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", status_code=201, response_model=ProductRead)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product: ProductUpdate, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/{product_id}", response_model=ProductRead)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(db_product)
    session.commit()
    return db_product