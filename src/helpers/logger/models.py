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
    """
    LogEntry represents a log entry in the database.

    This model stores log entries, including the timestamp, log level, and log message.

    Attributes:
        id (int): The primary key for the log entry record.
        timestamp (DateTime): The timestamp when the log entry was created.
        level (LogLevel): The log level (e.g., INFO, ERROR).
        message (JSON): The log message in JSON format.

    """

    __tablename__ = "log_entries"

    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(Enum(LogLevel), nullable=False)
    message = Column(JSON)
