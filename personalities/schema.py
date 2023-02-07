import datetime
from pydantic import Field


# Define fields to be stored in database
'''Schema to store personalities'''


class PersonalitiesSchema:
    timestamp: datetime.datetime
    name: str = Field(...)
    personality_id = str = Field(...)
    

'''Schema to store information of files where our solution result in an error'''


class ErrorSchema:
    timestamp: datetime.datetime
    Error: str = Field(...)
    TypeError: str = Field(...)
    ErrorFile: str = Field(...)
    ErrorLine: int = Field(...)
