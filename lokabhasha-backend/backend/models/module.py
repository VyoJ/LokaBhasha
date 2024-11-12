from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# TODO: Add Foreign Key constraints properly for language and module
class Module(Base):
    __tablename__ = "modules"

    m_id = Column(Integer, primary_key=True, index=True)
    lang_id = Column(Integer, ForeignKey("languages.lang_id"), nullable=False)
    name = Column(String(100), nullable=False)
    desc = Column(String(500), nullable=False)
    pre_id = Column(Integer, ForeignKey("modules.m_id"), nullable=True)
    language = relationship("Language", back_populates="modules")
    prerequisites = relationship("Module", remote_side=[m_id])
