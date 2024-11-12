from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.utils.database import Base


class Language(Base):
    __tablename__ = "languages"
    lang_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    users = relationship("User", back_populates="language")
    modules = relationship(
        "Module", back_populates="language", cascade="all, delete-orphan"
    )
