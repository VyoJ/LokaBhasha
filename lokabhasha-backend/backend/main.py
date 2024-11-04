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
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

encoded_password = quote_plus(DB_PASSWORD)

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
)
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


class LanguageCreate(BaseModel):
    name: str


class LanguageUpdate(BaseModel):
    name: Optional[str] = None


class LanguageInDB(BaseModel):
    lang_id: int
    name: str

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


@app.post("/languages/", response_model=LanguageInDB)
def create_language(language: LanguageCreate, db: Session = Depends(get_db)):
    # Check if language already exists
    db_language = db.query(Language).filter(Language.name == language.name).first()
    if db_language:
        raise HTTPException(status_code=400, detail="Language already exists")

    db_language = Language(name=language.name)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


@app.get("/languages/", response_model=List[LanguageInDB])
def read_languages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    languages = db.query(Language).offset(skip).limit(limit).all()
    return languages


@app.get("/languages/{lang_id}", response_model=LanguageInDB)
def read_language(lang_id: int, db: Session = Depends(get_db)):
    db_language = db.query(Language).filter(Language.lang_id == lang_id).first()
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_language


@app.put("/languages/{lang_id}", response_model=LanguageInDB)
def update_language(
    lang_id: int, language: LanguageUpdate, db: Session = Depends(get_db)
):
    db_language = db.query(Language).filter(Language.lang_id == lang_id).first()
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")

    # Check if the new name already exists (if name is being updated)
    if language.name:
        existing_language = (
            db.query(Language)
            .filter(Language.name == language.name, Language.lang_id != lang_id)
            .first()
        )
        if existing_language:
            raise HTTPException(status_code=400, detail="Language name already exists")

    for var, value in vars(language).items():
        if value is not None:
            setattr(db_language, var, value)

    db.commit()
    db.refresh(db_language)
    return db_language


@app.delete("/languages/{lang_id}", response_model=LanguageInDB)
def delete_language(lang_id: int, db: Session = Depends(get_db)):
    db_language = db.query(Language).filter(Language.lang_id == lang_id).first()
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")

    # Check if any users are using this language as their preferred language
    users_with_language = db.query(User).filter(User.pref_lang == lang_id).first()
    if users_with_language:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete language as it is being used as preferred language by some users",
        )

    db.delete(db_language)
    db.commit()
    return db_language


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
