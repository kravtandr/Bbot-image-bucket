from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CommandData(BaseModel):
    linear: float
    angular: float
    experts: List[float]
    task_completed: bool

class RecordBase(BaseModel):
    command: CommandData

class RecordCreate(RecordBase):
    pass

class Record(RecordBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True