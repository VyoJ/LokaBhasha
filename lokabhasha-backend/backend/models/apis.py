from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class API(Base):
    __tablename__ = "APIs"

    api_id = Column(Integer, primary_key=True, index=True)
    api_url = Column(String(50), nullable=False)
    lang_id = Column(Integer, nullable=False)
