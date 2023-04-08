from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models import *
from database import Session, get_session


router = APIRouter(tags=["Accounts"], prefix="/accounts")

@router.get("/", response_model=List[AccountRead])
def get_accounts(limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    db_accounts = session.query(Account).offset(offset).limit(limit).all()
    if not db_accounts:
        raise HTTPException(status_code=404, detail="No accounts found")
    return db_accounts

@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: int, session: Session = Depends(get_session)):
    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.post("/", status_code=201, response_model=AccountRead)
def create_account(account: AccountCreate, session: Session = Depends(get_session)):
    db_account = Account(**account.dict())
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account

@router.patch("/{account_id}", response_model=AccountRead)
def update_account(account_id: int, account: AccountUpdate, session: Session = Depends(get_session)):
    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in account.dict(exclude_unset=True).items():
        setattr(db_account, key, value)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account

@router.delete("/{account_id}", response_model=AccountRead)
def delete_account(account_id: int, session: Session = Depends(get_session)):
    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(db_account)
    session.commit()
    return db_account