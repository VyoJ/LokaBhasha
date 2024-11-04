from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate
from datetime import datetime


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


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.u_id == user_id).first()


def update_user(db: Session, db_user: User, user: UserUpdate):
    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return db_user
