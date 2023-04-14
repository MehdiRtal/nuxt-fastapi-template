from fastapi import APIRouter, HTTPException
from typing import List

from models import Order, OrderCreate, OrderRead, OrderUpdate
from database import DBSession


router = APIRouter(tags=["Orders"], prefix="/orders")

@router.get("/", response_model=List[OrderRead])
def get_orders(db_session: DBSession, limit: int = 100, offset: int = 0):
    db_orders = db_session.query(Order).offset(offset).limit(limit).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return db_orders

@router.get("/{order_id}", response_model=OrderRead)
def get_order(db_session: DBSession, order_id: int):
    db_order = db_session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/", status_code=201, response_model=OrderRead)
def create_order(db_session: DBSession, order: OrderCreate):
    db_order = Order(**order.dict())
    db_session.add(db_order)
    db_session.commit()
    db_session.refresh(db_order)
    return db_order

@router.patch("/{order_id}", response_model=OrderRead)
def update_order(db_session: DBSession, order_id: int, order: OrderUpdate):
    db_order = db_session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    db_session.add(db_order)
    db_session.commit()
    db_session.refresh(db_order)
    return db_order

@router.delete("/{order_id}", response_model=OrderRead)
def delete_order(db_session: DBSession, order_id: int):
    db_order = db_session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_session.delete(db_order)
    db_session.commit()
    return db_order