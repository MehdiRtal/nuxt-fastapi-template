from fastapi import APIRouter, HTTPException
from typing import List

from models import Category, CategoryCreate, CategoryRead, CategoryUpdate
from databases import Database


router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/", response_model=List[CategoryRead])
def get_categories(db: Database, limit: int = 100, offset: int = 0):
    db_categories = db.query(Category).offset(offset).limit(limit).all()
    if not db_categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return db_categories

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(db: Database, category_id: int):
    db_category = db.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/", status_code=201, response_model=CategoryRead)
def add_category(db: Database, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(db: Database, category_id: int, category: CategoryUpdate):
    db_category = db.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(db: Database, category_id: int):
    db_category = db.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category