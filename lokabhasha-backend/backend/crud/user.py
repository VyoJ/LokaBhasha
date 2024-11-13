from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.utils.models import User
from backend.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        joined_on=datetime.now(),
        pref_lang=user.pref_lang,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_id: int, full_object: bool = False):
    query = db.query(User).filter(User.u_id == user_id)

    if not full_object:
        return query.with_entities(
            User.u_id, User.username, User.email, User.joined_on, User.pref_lang
        ).first()
    return query.first()


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.u_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)
    if "password" in user_data:
        user_data["password"] = pwd_context.hash(user_data["password"])
    for field, value in user_data.items():
        setattr(db_user, field, value)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return db_user
