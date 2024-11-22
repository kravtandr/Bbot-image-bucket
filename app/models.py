from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from .database import Base
import datetime

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(JSON)  # Изменено на JSON тип
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)