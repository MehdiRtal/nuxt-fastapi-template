from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models import *
from database import Session, get_session


router = APIRouter(tags=["Orders"], prefix="/orders")

@router.get("/", response_model=List[OrderRead])
def get_orders(limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    db_orders = session.query(Order).offset(offset).limit(limit).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return db_orders

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/", status_code=201, response_model=OrderRead)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.dict())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.patch("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order: OrderUpdate, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.delete("/{order_id}", response_model=OrderRead)
def delete_order(order_id: int, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(db_order)
    session.commit()
    return db_order