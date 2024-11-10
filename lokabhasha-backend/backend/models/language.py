# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


# class Language(Base):
#     __tablename__ = "Languages"
#     lang_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), unique=True, nullable=False)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.utils.database import Base

class Language(Base):
    __tablename__ = "languages"
    lang_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    users = relationship("User", back_populates="language")  # Define relationship back to User