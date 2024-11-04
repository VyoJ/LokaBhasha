from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Language(Base):
    __tablename__ = "Languages"
    lang_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
