from typing import List
from backend.utils.models import Response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.responses import ResponseCreate, ResponseUpdate, ResponseInDB
from backend.crud.responses import (
    create_response,
    get_response,
    update_response,
    delete_response,
)
from backend.utils.database import get_db

router = APIRouter()


@router.post("/responses/", response_model=ResponseInDB)
def create_response_endpoint(response: ResponseCreate, db: Session = Depends(get_db)):
    return create_response(db, response)


@router.get("/responses/", response_model=List[ResponseInDB])
def read_responses_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Response).offset(skip).limit(limit).all()


@router.get("/responses/{resp_id}", response_model=ResponseInDB)
def read_response_endpoint(resp_id: int, db: Session = Depends(get_db)):
    db_response = get_response(db, resp_id)
    if db_response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return db_response


@router.put("/responses/{resp_id}", response_model=ResponseInDB)
def update_response_endpoint(
    resp_id: int, response: ResponseUpdate, db: Session = Depends(get_db)
):
    db_response = get_response(db, resp_id)
    if db_response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return update_response(db, db_response, response)


@router.delete("/responses/{resp_id}", response_model=ResponseInDB)
def delete_response_endpoint(resp_id: int, db: Session = Depends(get_db)):
    db_response = get_response(db, resp_id)
    if db_response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return delete_response(db, db_response)
