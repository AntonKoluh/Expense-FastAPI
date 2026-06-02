from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.database import get_db
from models.users import Users
from models.categories import Categories
from models.transactions import Transactions
from helpers.auth_dependencies import get_current_user
from schemas.transactions import TransactionRead, TransactionWrite

router = APIRouter()

@router.get("/transaction", response_model=list[TransactionRead])
def get_transaction(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    if user.is_staff:
        transaction = db.query(Transactions).all()
    else:
        transaction = db.query(Transactions).filter(Transactions.user_id == user.id).all()

    return transaction

@router.post("/transaction", response_model=TransactionRead)
def create_transaction(new_transaction: TransactionWrite,
                    db: Session = Depends(get_db),
                    user: Users = Depends(get_current_user)):
    
    categories = []
    for category_name in new_transaction.categories:
        category = (
            db.query(Categories)
            .filter(
                Categories.name==category_name,
                Categories.user_id==user.id
                )
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=400,
                detail=f"Error, category {category_name} does not exist"
            )

        if category.limit and new_transaction.amount > category.limit:
            raise HTTPException(
                status_code=400,
                detail=f"limit on category {category.name}({category.limit}) is exceeded by this operation ({new_transaction.amount})"
            )
        
        categories.append(category)

    transaction = Transactions(
        name=new_transaction.name,
        amount=new_transaction.amount,
        categories=categories,
        user_id=user.id
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction