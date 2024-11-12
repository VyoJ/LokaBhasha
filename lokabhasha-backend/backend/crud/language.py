from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.models.language import Language
from backend.schemas.language import LanguageBase, LanguageUpdate


def create_language(db: Session, language: LanguageBase):
    db_language = Language(name=language.name)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def get_language(db: Session, lang_id: int):
    return db.query(Language).filter(Language.lang_id == lang_id).first()


def update_language(db: Session, db_language: Language, language: LanguageUpdate):
    for var, value in vars(language).items():
        if value is not None:
            setattr(db_language, var, value)
    db.commit()
    db.refresh(db_language)
    return db_language


def reset_language_id_sequence(db: Session):
    db.execute(text("ALTER TABLE Languages AUTO_INCREMENT = 1"))
    db.commit()


def delete_language(db: Session, db_language: Language):
    db.delete(db_language)
    db.commit()
