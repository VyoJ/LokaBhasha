from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class API(Base):
    __tablename__ = "APIs"

    api = Column(String(50), primary_key=True, index=True)
    lang_id = Column(Integer, nullable=False)