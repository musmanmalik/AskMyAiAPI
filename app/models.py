from sqlalchemy import Column, Integer, String, DateTime , Uuid, Boolean
from app.database import Base


class Log(Base):
    __tablename__ = "api_log"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime)
    question = Column(String)
    question_id = Column(Uuid(as_uuid=True),  unique=True)
    context_id = Column(String)
    context_source = Column(String)


class Feedback(Base):
    __tablename__ = "api_feedback"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime)
    question_id = Column(Uuid(as_uuid=True),  unique=True)
    person = Column(String)
    question = Column(String)
    answer = Column(String)
    feedback = Column(Integer, default=0)
