from typing import List
from backend.utils.models import API
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.apis import APICreate, APIUpdate, APIInDB
from backend.crud.apis import (
    create_api,
    get_api,
    update_api,
    delete_api,
)
from backend.utils.database import get_db

router = APIRouter()

@router.post("/apis/", response_model=APIInDB)
def create_api_endpoint(api: APICreate, db: Session = Depends(get_db)):
    return create_api(db, api)

@router.get("/apis/", response_model=List[APIInDB])
def read_apis_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(API).offset(skip).limit(limit).all()

@router.get("/apis/{api_id}", response_model=APIInDB)
def read_api_endpoint(api_id: int, db: Session = Depends(get_db)):
    db_api = get_api(db, api_id)
    if db_api is None:
        raise HTTPException(status_code=404, detail="API not found")
    return db_api

@router.put("/apis/{api_id}", response_model=APIInDB)
def update_api_endpoint(
    api_id: int, api: APIUpdate, db: Session = Depends(get_db)
):
    db_api = get_api(db, api_id)
    if db_api is None:
        raise HTTPException(status_code=404, detail="API not found")
    return update_api(db, db_api, api)

@router.delete("/apis/{api_id}", response_model=APIInDB)
def delete_api_endpoint(api_id: str, db: Session = Depends(get_db)):
    db_api = get_api(db, api_id)
    if db_api is None:
        raise HTTPException(status_code=404, detail="API not found")
    return delete_api(db, db_api)