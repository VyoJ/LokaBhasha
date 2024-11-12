from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.utils.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    joined_on = Column(DateTime, nullable=False)
    pref_lang = Column(Integer, ForeignKey("languages.lang_id"))
    language = relationship("Language", back_populates="users")
