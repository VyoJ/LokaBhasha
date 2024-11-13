from sqlalchemy.orm import Session
from backend.utils.models import Response
from backend.schemas.responses import ResponseCreate, ResponseUpdate


def create_response(db: Session, response: ResponseCreate):
    db_response = Response(
        response_asr=response.response_asr,
        response_url=response.response_url,
        response_translate=response.response_translate,
        latency=response.latency,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_response(db: Session, resp_id: int):
    return db.query(Response).filter(Response.resp_id == resp_id).first()


def update_response(db: Session, db_response: Response, response: ResponseUpdate):
    for var, value in vars(response).items():
        if value is not None:
            setattr(db_response, var, value)
    db.commit()
    db.refresh(db_response)
    return db_response


def delete_response(db: Session, db_response: Response):
    db.delete(db_response)
    db.commit()
    return db_response
