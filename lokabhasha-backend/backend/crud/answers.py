from sqlalchemy.orm import Session
from backend.models.answers import Answer
from backend.schemas.answers import AnswerCreate, AnswerUpdate

def create_answer(db: Session, answer: AnswerCreate):
    db_answer = Answer(q_id=answer.q_id, resp_id=answer.resp_id, u_id=answer.u_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_answer(db: Session, q_id: int, resp_id: int):
    return db.query(Answer).filter(Answer.q_id == q_id, Answer.resp_id == resp_id).first()

def update_answer(db: Session, db_answer: Answer, answer: AnswerUpdate):
    for var, value in vars(answer).items():
        if value is not None:
            setattr(db_answer, var, value)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()
    return db_answer