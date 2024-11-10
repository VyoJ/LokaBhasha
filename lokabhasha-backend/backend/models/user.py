# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "Users"
#     u_id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, nullable=False)
#     email = Column(String(100), unique=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     joined_on = Column(DateTime, nullable=False)
#     pref_lang = Column(Integer, ForeignKey("Languages.lang_id"))
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.utils.database import Base

class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    joined_on = Column(DateTime, nullable=False)
    pref_lang = Column(Integer, ForeignKey('languages.lang_id'), nullable=True)
    role = Column(String, default="user")
    language = relationship("Language", back_populates="users")  # Use string-based lazy relationship