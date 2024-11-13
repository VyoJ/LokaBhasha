from sqlalchemy.orm import Session
from backend.utils.models import Module
from backend.schemas.module import ModuleCreate, ModuleUpdate


def create_module(db: Session, module: ModuleCreate):
    db_module = Module(
        lang_id=module.lang_id, name=module.name, desc=module.desc, pre_id=module.pre_id
    )
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module


def get_module(db: Session, module_id: int):
    return db.query(Module).filter(Module.m_id == module_id).first()


def update_module(db: Session, db_module: Module, module: ModuleUpdate):
    for var, value in vars(module).items():
        if value is not None:
            setattr(db_module, var, value)
    db.commit()
    db.refresh(db_module)
    return db_module


def delete_module(db: Session, db_module: Module):
    db.delete(db_module)
    db.commit()
    return db_module
