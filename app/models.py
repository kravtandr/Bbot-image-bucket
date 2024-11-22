from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
import datetime

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    find_goal = Column(Boolean, default=True)