from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from db.database import get_db
from models.users import Users
from helpers.passwords import get_password_hash, verify_password
from helpers.auth import create_access_token
from helpers.auth_dependencies import get_current_user
from schemas.users import (
    UserRead,
    UserLoginRespose,
    UserLoginPost,
    UserCreate
    )

router = APIRouter()

@router.post("/get_auth_token", response_model=UserLoginRespose)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(Users)
        .filter(Users.username == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/users", response_model=list[UserRead] | UserRead)
async def get_users(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    if user.is_staff:
        user_res = db.query(Users).all()
    else:
        user_res = db.query(Users).filter(Users.id == user.id).first()

    return user_res

@router.post("/users", response_model=UserRead)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(Users)
        .filter(Users.username == user_data.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="username already exists"
        )
    
    user = Users(
        username=user_data.username,
        password=get_password_hash(user_data.password),
        is_staff=user_data.is_staff
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user