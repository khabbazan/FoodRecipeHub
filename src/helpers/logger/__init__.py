from src.core.database import local_session
from src.helpers.logger.models import LogEntry


class LoggerSingletonMeta(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(LoggerSingletonMeta, cls).__call__()
        return cls._instances[cls]


class Logger(metaclass=LoggerSingletonMeta):
    """
    Logger is a singleton class for managing log entries in the database.

    This class provides a simple mechanism for adding log entries to the database. It is designed as a singleton to ensure
    that there is only one instance of the logger throughout the application.

    Example usage:

    ```python
    logger.log(level=LogLevel.INFO, message="Log message")
    ```

    Methods:
        log(level, message):
            Adds a log entry to the database with the specified log level and message.

    """

    def __init__(self):
        self.Session = local_session

    def log(self, level, message):
        """
        Add a log entry to the database.

        Args:
            level (LogLevel): The log level (e.g., LogLevel.INFO).
            message (str): The log message.

        Example usage:

        ```python
        logger = Logger()
        logger.log(level=LogLevel.INFO, message="Log message")
        ```

        """
        entry = LogEntry(level=level, message=message)
        session = self.Session()
        session.add(entry)
        session.commit()
        session.refresh(entry)


logger = Logger()
