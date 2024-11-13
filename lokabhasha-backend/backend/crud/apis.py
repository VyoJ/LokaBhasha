from sqlalchemy.orm import Session
from backend.utils.models import API
from backend.schemas.apis import APICreate, APIUpdate


def create_api(db: Session, api: APICreate):
    db_api = API(api_url=api.api_url, lang_id=api.lang_id)
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    return db_api


def get_api(db: Session, api_id: int):
    return db.query(API).filter(API.api_id == api_id).first()


def update_api(db: Session, db_api: API, api: APIUpdate):
    for var, value in vars(api).items():
        if value is not None:
            setattr(db_api, var, value)
    db.commit()
    db.refresh(db_api)
    return db_api


def delete_api(db: Session, db_api: API):
    db.delete(db_api)
    db.commit()
    return db_api
