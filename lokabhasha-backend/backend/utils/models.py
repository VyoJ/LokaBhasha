from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    resources = relationship(
        "Resource", back_populates="language", cascade="all, delete-orphan"
    )
    apis = relationship("API", back_populates="language")


class User(Base):
    __tablename__ = "users"

    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    joined_on = Column(DateTime, nullable=False)
    pref_lang = Column(Integer, ForeignKey("languages.lang_id"))

    language = relationship("Language", back_populates="users")


class Module(Base):
    __tablename__ = "modules"

    m_id = Column(Integer, primary_key=True, index=True)
    lang_id = Column(Integer, ForeignKey("languages.lang_id"), nullable=False)
    name = Column(String(100), nullable=False)
    desc = Column(String(500), nullable=False)
    pre_id = Column(Integer, ForeignKey("modules.m_id"), nullable=True)

    prerequisites = relationship("Module", remote_side=[m_id])
    language = relationship("Language", back_populates="modules")
    questions = relationship(
        "Question", back_populates="modules", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    q_id = Column(Integer, primary_key=True, index=True)
    m_id = Column(Integer, ForeignKey("modules.m_id"), nullable=False)
    question = Column(String(500), nullable=False)
    exp_ans = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)

    modules = relationship("Module", back_populates="questions")
    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )


class Response(Base):
    __tablename__ = "Responses"

    resp_id = Column(Integer, primary_key=True, index=True)
    response_asr = Column(String(500), nullable=False)
    response_url = Column(String(500), nullable=False)
    response_translate = Column(String(500), nullable=False)
    latency = Column(Integer, nullable=False)

    answers = relationship("Answer", back_populates="response")


class Answer(Base):
    __tablename__ = "Answers"

    q_id = Column(Integer, ForeignKey("questions.q_id"), primary_key=True, index=True)
    resp_id = Column(
        Integer, ForeignKey("Responses.resp_id"), primary_key=True, index=True
    )
    u_id = Column(Integer, ForeignKey("users.u_id"), nullable=False)

    question = relationship("Question", back_populates="answers")
    response = relationship("Response", back_populates="answers")


class Resource(Base):
    __tablename__ = "Resources"

    lang_id = Column(
        Integer,
        ForeignKey("languages.lang_id"),
        primary_key=True,
        index=True,
        onupdate="CASCADE",
    )
    resource_id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)
    format = Column(String(50), nullable=False)

    language = relationship("Language", back_populates="resources")


class API(Base):
    __tablename__ = "APIs"

    api_id = Column(Integer, primary_key=True, index=True)
    api_url = Column(String(50), nullable=False)
    lang_id = Column(Integer, ForeignKey("languages.lang_id"), nullable=False)

    language = relationship("Language", back_populates="apis")
