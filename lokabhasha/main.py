from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

SQLALCHEMY_DATABASE_URL = "mysql://root:Root@604@localhost/lokabhasha"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "Users"
    u_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    joined_on = Column(DateTime, nullable=False)
    pref_lang = Column(Integer, ForeignKey("Languages.lang_id"))


class Language(Base):
    __tablename__ = "Languages"
    lang_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)


# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    pref_lang: Optional[int] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    pref_lang: Optional[int] = None


class UserInDB(BaseModel):
    u_id: int
    username: str
    email: str
    joined_on: datetime
    pref_lang: Optional[int] = None

    class Config:
        orm_mode = True


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD operations for User
@app.post("/users/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
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


@app.get("/users/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.u_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.u_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=UserInDB)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.u_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
