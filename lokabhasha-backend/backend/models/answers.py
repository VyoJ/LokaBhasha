from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Answer(Base):
    __tablename__ = "Answers"

    q_id = Column(Integer, ForeignKey("Questions.q_id"), primary_key=True, index=True)
    resp_id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey("Users.u_id"), nullable=False)