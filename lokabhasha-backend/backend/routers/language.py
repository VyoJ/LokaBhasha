from typing import List
from backend.models.language import Language
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.language import LanguageCreate, LanguageUpdate, LanguageInDB
from backend.crud.language import (
    create_language,
    get_language,
    update_language,
    delete_language,
)
from backend.utils.database import get_db

router = APIRouter()


@router.post("/languages/", response_model=LanguageInDB)
def create_language_endpoint(language: LanguageCreate, db: Session = Depends(get_db)):
    return create_language(db, language)


@router.get("/languages/", response_model=List[LanguageInDB])
def read_languages_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Language).offset(skip).limit(limit).all()


@router.get("/languages/{lang_id}", response_model=LanguageInDB)
def read_language_endpoint(lang_id: int, db: Session = Depends(get_db)):
    db_language = get_language(db, lang_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_language


@router.put("/languages/{lang_id}", response_model=LanguageInDB)
def update_language_endpoint(
    lang_id: int, language: LanguageUpdate, db: Session = Depends(get_db)
):
    db_language = get_language(db, lang_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return update_language(db, db_language, language)


@router.delete("/languages/{lang_id}", response_model=LanguageInDB)
def delete_language_endpoint(lang_id: int, db: Session = Depends(get_db)):
    db_language = get_language(db, lang_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return delete_language(db, db_language)
