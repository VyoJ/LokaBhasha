from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate, UserUpdate, UserInDB
from backend.crud.user import create_user, get_user, update_user, delete_user
from backend.utils.database import get_db

router = APIRouter()


@router.post("/users/", response_model=UserInDB)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users/{user_id}", response_model=UserInDB)
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=UserInDB)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, db_user, user)


@router.delete("/users/{user_id}", response_model=UserInDB)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db, db_user)
