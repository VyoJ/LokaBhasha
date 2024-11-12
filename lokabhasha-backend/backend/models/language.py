from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.utils.database import Base

# TODO: Write a trigger to fix auto-increment when things are deleted
class Language(Base):
    __tablename__ = "languages"
    lang_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    users = relationship("User", back_populates="language")
