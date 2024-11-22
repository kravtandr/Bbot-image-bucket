from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecordBase(BaseModel):
    command: str
    find_goal: bool

class RecordCreate(RecordBase):
    pass

class Record(RecordBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True