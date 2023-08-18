from fastapi import APIRouter, HTTPException
from typing import List

from models import Order, OrderCreate, OrderRead, OrderUpdate
from databases import Database


router = APIRouter(tags=["Orders"], prefix="/orders")

@router.get("/", response_model=List[OrderRead])
def get_orders(db: Database, limit: int = 100, offset: int = 0):
    db_orders = db.query(Order).offset(offset).limit(limit).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return db_orders

@router.get("/{order_id}", response_model=OrderRead)
def get_order(db: Database, order_id: int):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/", status_code=201, response_model=OrderRead)
def add_order(db: Database, order: OrderCreate):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.patch("/{order_id}", response_model=OrderRead)
def update_order(db: Database, order_id: int, order: OrderUpdate):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}", response_model=OrderRead)
def delete_order(db: Database, order_id: int):
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order