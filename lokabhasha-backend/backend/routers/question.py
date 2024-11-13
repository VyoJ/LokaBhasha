from typing import List
from backend.utils.models import Question
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.question import QuestionCreate, QuestionUpdate, QuestionInDB
from backend.crud.question import (
    create_question,
    get_question,
    update_question,
    delete_question,
)
from backend.utils.database import get_db

router = APIRouter()


@router.post("/questions/", response_model=QuestionInDB)
def create_question_endpoint(question: QuestionCreate, db: Session = Depends(get_db)):
    return create_question(db, question)


@router.get("/questions/", response_model=List[QuestionInDB])
def read_questions_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Question).offset(skip).limit(limit).all()


@router.get("/questions/{question_id}", response_model=QuestionInDB)
def read_question_endpoint(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.put("/questions/{question_id}", response_model=QuestionInDB)
def update_question_endpoint(
    question_id: int, question: QuestionUpdate, db: Session = Depends(get_db)
):
    db_question = get_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return update_question(db, db_question, question)


@router.delete("/questions/{question_id}", response_model=QuestionInDB)
def delete_question_endpoint(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return delete_question(db, db_question)
