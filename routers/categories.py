from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.database import get_db
from models.users import Users
from models.categories import Categories
from helpers.passwords import get_password_hash, verify_password
from helpers.auth import create_access_token
from helpers.auth_dependencies import get_current_user
from schemas.categories import CategoryRead, CategoryWrite

router = APIRouter()

@router.get("/categories", response_model=list[CategoryRead])
def get_categories(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    if user.is_staff:
        categories = db.query(Categories).all()
    else:
        categories = db.query(Categories).filter(Categories.user_id == user.id).all()

    return categories

@router.post("/categories", response_model=CategoryRead)
def create_category(new_category: CategoryWrite,
                    db: Session = Depends(get_db),
                    user: Users = Depends(get_current_user)):

    category_exists = (
        db.query(Categories)
        .filter(Categories.name==new_category.name, 
                Categories.user_id==user.id)
        .first()
    )

    if category_exists:
        raise HTTPException(
            status_code=400,
            detail=f"{new_category.name} already exist on {user.username}"
        )
    
    category = Categories(
        name=new_category.name,
        limit=new_category.limit,
        user_id=user.id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category