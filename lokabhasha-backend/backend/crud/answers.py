from sqlalchemy.orm import Session
from backend.utils.models import Answer


def get_answer(db: Session, q_id: int, resp_id: int):
    return (
        db.query(Answer).filter(Answer.q_id == q_id, Answer.resp_id == resp_id).first()
    )


def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()
    return db_answer
