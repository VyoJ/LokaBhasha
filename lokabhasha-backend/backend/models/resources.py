from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Resource(Base):
    __tablename__ = "Resources"

    lang_id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)
    format = Column(String(50), nullable=False)