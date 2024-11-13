from typing import List
from backend.utils.models import Answer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.answers import AnswerInDB
from backend.crud.answers import (
    get_answer,
    delete_answer,
)
from backend.utils.database import get_db

router = APIRouter()


@router.get("/answers/", response_model=List[AnswerInDB])
def read_answers_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Answer).offset(skip).limit(limit).all()


@router.get("/answers/{q_id}/{resp_id}", response_model=AnswerInDB)
def read_answer_endpoint(q_id: int, resp_id: int, db: Session = Depends(get_db)):
    db_answer = get_answer(db, q_id, resp_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_answer


@router.delete("/answers/{q_id}/{resp_id}", response_model=AnswerInDB)
def delete_answer_endpoint(q_id: int, resp_id: int, db: Session = Depends(get_db)):
    db_answer = get_answer(db, q_id, resp_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return delete_answer(db, db_answer)
