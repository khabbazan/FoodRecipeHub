import enum
from datetime import datetime
from sqlalchemy import Column, Integer, JSON, DateTime, Enum

from src.core.databse import Basemodel


class LogLevel(enum.Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"


class LogEntry(Basemodel):

    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(Enum(LogLevel), nullable=False)
    message = Column(JSON)
