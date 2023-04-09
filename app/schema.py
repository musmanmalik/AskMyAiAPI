from pydantic import BaseModel
from typing import Union
from uuid import UUID


import datetime


class Question(BaseModel):
    question: str
    name: Union[str, None] = None


class FeedBack(BaseModel):
    question_id: Union[UUID, None] = None
    feedback: Union[int, None] = None


class LogsBase(BaseModel):
    class Config:
        orm_mode = True


class FeedbackBase(BaseModel):
    class Config:
        orm_mode = True


class Logs(LogsBase):
    question: Union[str, None] = None
    question_id: Union[UUID, None] = None
    context_id: Union[str, None] = None
    context_source: Union[str, None] = None


class Feedbacks(FeedbackBase):
    question_id: Union[UUID, None] = None
    question: Union[str, None] = None
    person: Union[str, None] = None
    answer: Union[str, None] = None
    feedback: Union[int, None] = None
