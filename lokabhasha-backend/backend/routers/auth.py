from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate, UserInDB, UserLogin
from backend.crud.user import create_user, get_user_by_email, verify_password
from backend.utils.database import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO: Create JWT and send it as part of frontend response
@router.post("/signup", response_model=UserInDB)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    return create_user(db, user)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
