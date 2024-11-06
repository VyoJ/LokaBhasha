from typing import List
from backend.models.resources import Resource
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.resources import ResourceCreate, ResourceUpdate, ResourceInDB
from backend.crud.resources import (
    create_resource,
    get_resource,
    update_resource,
    delete_resource,
)
from backend.utils.database import get_db

router = APIRouter()

@router.post("/resources/", response_model=ResourceInDB)
def create_resource_endpoint(resource: ResourceCreate, db: Session = Depends(get_db)):
    return create_resource(db, resource)

@router.get("/resources/", response_model=List[ResourceInDB])
def read_resources_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Resource).offset(skip).limit(limit).all()

@router.get("/resources/{lang_id}/{resource_id}", response_model=ResourceInDB)
def read_resource_endpoint(lang_id: int, resource_id: int, db: Session = Depends(get_db)):
    db_resource = get_resource(db, lang_id, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.put("/resources/{lang_id}/{resource_id}", response_model=ResourceInDB)
def update_resource_endpoint(
    lang_id: int, resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)
):
    db_resource = get_resource(db, lang_id, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return update_resource(db, db_resource, resource)

@router.delete("/resources/{lang_id}/{resource_id}", response_model=ResourceInDB)
def delete_resource_endpoint(lang_id: int, resource_id: int, db: Session = Depends(get_db)):
    db_resource = get_resource(db, lang_id, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return delete_resource(db, db_resource)