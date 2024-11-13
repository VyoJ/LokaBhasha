from sqlalchemy.orm import Session
from backend.utils.models import Question
from backend.schemas.question import QuestionCreate, QuestionUpdate


def create_question(db: Session, question: QuestionCreate):
    db_question = Question(
        m_id=question.m_id,
        question=question.question,
        exp_ans=question.exp_ans,
        category=question.category,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.q_id == question_id).first()


def update_question(db: Session, db_question: Question, question: QuestionUpdate):
    update_data = question.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()
    return db_question
