from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.language import LanguageBase, LanguageUpdate, LanguageInDB
from backend.crud.language import (
    create_language,
    get_language,
    update_language,
    delete_language,
    reset_language_id_sequence,
)
from backend.utils.database import get_db
from backend.models.language import Language

router = APIRouter()

@router.post("/languages/", response_model=LanguageInDB)
def create_language_endpoint(language: LanguageBase, db: Session = Depends(get_db)):
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
    delete_language(db, db_language)  # Pass the Language instance
    reset_language_id_sequence(db)  # Reset the sequence after deletion
    return db_language