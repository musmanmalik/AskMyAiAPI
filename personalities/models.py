from typing import Union
from pydantic import BaseModel

class Question(BaseModel):
    question: str
    person_id: str
    question_id: str
    session_id: str
    name: Union[str, None] = None