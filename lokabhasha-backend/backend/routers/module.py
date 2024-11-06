from typing import List
from backend.models.module import Module
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.module import ModuleCreate, ModuleUpdate, ModuleInDB
from backend.crud.module import (
    create_module,
    get_module,
    update_module,
    delete_module,
)
from backend.utils.database import get_db

router = APIRouter()

@router.post("/modules/", response_model=ModuleInDB)
def create_module_endpoint(module: ModuleCreate, db: Session = Depends(get_db)):
    return create_module(db, module)

@router.get("/modules/", response_model=List[ModuleInDB])
def read_modules_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(Module).offset(skip).limit(limit).all()

@router.get("/modules/{module_id}", response_model=ModuleInDB)
def read_module_endpoint(module_id: int, db: Session = Depends(get_db)):
    db_module = get_module(db, module_id)
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module

@router.put("/modules/{module_id}", response_model=ModuleInDB)
def update_module_endpoint(
    module_id: int, module: ModuleUpdate, db: Session = Depends(get_db)
):
    db_module = get_module(db, module_id)
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return update_module(db, db_module, module)

@router.delete("/modules/{module_id}", response_model=ModuleInDB)
def delete_module_endpoint(module_id: int, db: Session = Depends(get_db)):
    db_module = get_module(db, module_id)
    if db_module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return delete_module(db, db_module)