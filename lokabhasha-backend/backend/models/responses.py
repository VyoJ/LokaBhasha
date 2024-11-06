from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Response(Base):
    __tablename__ = "Responses"

    resp_id = Column(Integer, primary_key=True, index=True)
    response_asr = Column(String(500), nullable=False)
    response_url = Column(String(500), nullable=False)
    response_translate = Column(String(500), nullable=False)
    latency = Column(Integer, nullable=False)