from fastapi import APIRouter, HTTPException, Depends
from typing import List

from models import *
from database import Session, get_session


router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/", response_model=List[CategoryRead])
def get_categories(limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    db_categories = session.query(Category).offset(offset).limit(limit).all()
    if not db_categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return db_categories

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, session: Session = Depends(get_session)):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/", status_code=201, response_model=CategoryRead)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    db_category = Category(**category.dict())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category: CategoryUpdate, session: Session = Depends(get_session)):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(category_id: int, session: Session = Depends(get_session)):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(db_category)
    session.commit()
    return db_category