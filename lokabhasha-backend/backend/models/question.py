from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    q_id = Column(Integer, primary_key=True, index=True)
    m_id = Column(Integer, ForeignKey("Modules.m_id"), nullable=False)
    question = Column(String(500), nullable=False)
    exp_ans = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)
    modules = relationship(
        "Module", back_populates="questions", cascade="all, delete-orphan"
    )
