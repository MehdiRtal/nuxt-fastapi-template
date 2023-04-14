from fastapi import APIRouter, HTTPException
from typing import List

from models import *
from database import DBSession


router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/", response_model=List[CategoryRead])
def get_categories(db_session: DBSession, limit: int = 100, offset: int = 0):
    db_categories = db_session.query(Category).offset(offset).limit(limit).all()
    if not db_categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return db_categories

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(db_session: DBSession, category_id: int):
    db_category = db_session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/", status_code=201, response_model=CategoryRead)
def create_category(db_session: DBSession, category: CategoryCreate):
    db_category = Category(**category.dict())
    db_session.add(db_category)
    db_session.commit()
    db_session.refresh(db_category)
    return db_category

@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(db_session: DBSession, category_id: int, category: CategoryUpdate):
    db_category = db_session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db_session.add(db_category)
    db_session.commit()
    db_session.refresh(db_category)
    return db_category

@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(db_session: DBSession, category_id: int):
    db_category = db_session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_session.delete(db_category)
    db_session.commit()
    return db_category