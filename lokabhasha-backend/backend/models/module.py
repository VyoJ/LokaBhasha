from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Module(Base):
    __tablename__ = "Modules"

    m_id = Column(Integer, primary_key=True, index=True)
    lang_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    desc = Column(String(500), nullable=False)
    pre_id = Column(Integer, nullable=True)