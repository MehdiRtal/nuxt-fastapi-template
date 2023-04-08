from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from models import *
from database import Session, get_session
from dependencies import CurrentUser
from utils import pwd_context, create_payment


router = APIRouter(tags=["Users"], prefix="/users")

@router.get("/me/accounts", response_model=List[AccountRead])
def get_current_user_accounts(current_user: CurrentUser, limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    statement = select(Account).where(Account.user_id == current_user.id).offset(offset).limit(limit)
    db_accounts = session.exec(statement).all()
    if not db_accounts:
        raise HTTPException(status_code=404, detail="No accounts found")
    return db_accounts

@router.get("/me/accounts/{account_id}", response_model=AccountRead)
def get_current_user_account(current_user: CurrentUser, account_id: int, session: Session = Depends(get_session)):
    statement = select(Account).where(Account.user_id == current_user.id).where(Account.id == account_id)
    db_account = session.exec(statement).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.post("/me/accounts", status_code=201, response_model=AccountRead)
def create_current_user_account(current_user: CurrentUser, account: AccountCreate, session: Session = Depends(get_session)):
    account.user_id = current_user.id 
    db_account = Account(**account.dict())
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account

@router.patch("/me/accounts/{account_id}", response_model=AccountRead)
def update_current_user_account(current_user: CurrentUser, account_id: int, account: AccountUpdate, session: Session = Depends(get_session)):
    statement = select(Account).where(Account.user_id == current_user.id).where(Account.id == account_id)
    db_account = session.exec(statement).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in account.dict(exclude_unset=True).items():
        setattr(db_account, key, value)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account

@router.delete("/me/accounts/{account_id}", response_model=AccountRead)
def delete_current_user_account(current_user: CurrentUser, account_id: int, session: Session = Depends(get_session)):
    statement = select(Account).where(Account.user_id == current_user.id).where(Account.id == account_id)
    db_account = session.exec(statement).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(db_account)
    session.commit()
    return db_account

@router.get("/me/orders", response_model=List[OrderRead])
def get_current_user_orders(current_user: CurrentUser, limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    statement = select(Order).where(Order.user_id == current_user.id).offset(offset).limit(limit)
    db_orders = session.exec(statement).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return db_orders

@router.get("/me/orders/{order_id}", response_model=OrderRead)
def get_current_user_order(current_user: CurrentUser, order_id: int, session: Session = Depends(get_session)):
    statement = select(Order).where(Order.user_id == current_user.id).where(Order.id == order_id)
    db_order = session.exec(statement).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/me/orders", status_code=201, response_model=OrderRead)
def create_current_user_order(current_user: CurrentUser, background_tasks: BackgroundTasks, order: OrderCreate, session: Session = Depends(get_session)):
    order.user_id = current_user.id
    db_product = session.get(Product, order.product_id)
    current_user.balance -= db_product.price * order.quantity
    db_order = Order(**order.dict())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.patch("/me/orders/{order_id}", response_model=OrderRead)
def update_current_user_order(current_user: CurrentUser, order_id: int, order: OrderUpdate, session: Session = Depends(get_session)):
    statement = select(Order).where(Order.user_id == current_user.id).where(Order.id == order_id)
    db_order = session.exec(statement).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.delete("/me/orders/{order_id}", response_model=OrderRead)
def delete_current_user_order(current_user: CurrentUser, order_id: int, session: Session = Depends(get_session)):
    statement = select(Order).where(Order.user_id == current_user.id).where(Order.id == order_id)
    db_order = session.exec(statement).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(db_order)
    session.commit()
    return db_order

@router.post("/me/change-password", response_model=UserRead)
def change_current_user_password(current_user: CurrentUser, current_password: str, new_password: str, session: Session = Depends(get_session)):
    if not pwd_context.verify(current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    current_user.password = pwd_context.hash(new_password)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.get("/me/buy-credits", response_class=RedirectResponse)
def buy_current_user_credits(current_user: CurrentUser, quantity: int):
    return create_payment(quantity, current_user.email, {"user_id": current_user.id})

@router.get("/me", response_model=UserRead)
def get_current_user(current_user: CurrentUser):
    return current_user

@router.patch("/me", response_model=UserRead)
def update_current_user(current_user: CurrentUser, user: UserUpdate, session: Session = Depends(get_session)):
    for key, value in user.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.delete("/me", response_model=UserRead)
def delete_current_user(current_user: CurrentUser, session: Session = Depends(get_session)):
    session.delete(current_user)
    session.commit()
    return current_user

@router.get("/", response_model=List[UserRead])
def get_users(limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    db_users = session.query(User).offset(offset).limit(limit).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="No users found")
    return db_users

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", status_code=201, response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return db_user