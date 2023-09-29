import enum
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy import Enum

from src.core.database import Basemodel


class LogLevel(enum.Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"


class LogEntry(Basemodel):

    __tablename__ = "log_entries"

    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(Enum(LogLevel), nullable=False)
    message = Column(JSON)
