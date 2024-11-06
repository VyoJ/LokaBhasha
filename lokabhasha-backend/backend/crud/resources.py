from sqlalchemy.orm import Session
from backend.models.resources import Resource
from backend.schemas.resources import ResourceCreate, ResourceUpdate

def create_resource(db: Session, resource: ResourceCreate):
    db_resource = Resource(lang_id=resource.lang_id, resource_id=resource.resource_id, url=resource.url, type=resource.type, format=resource.format)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def get_resource(db: Session, lang_id: int, resource_id: int):
    return db.query(Resource).filter(Resource.lang_id == lang_id, Resource.resource_id == resource_id).first()

def update_resource(db: Session, db_resource: Resource, resource: ResourceUpdate):
    for var, value in vars(resource).items():
        if value is not None:
            setattr(db_resource, var, value)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def delete_resource(db: Session, db_resource: Resource):
    db.delete(db_resource)
    db.commit()
    return db_resource