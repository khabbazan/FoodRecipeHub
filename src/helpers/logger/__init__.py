from src.core.database import local_session
from src.helpers.logger.models import LogEntry


class LoggerSingletonMeta(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(LoggerSingletonMeta, cls).__call__()
        return cls._instances[cls]


class Logger(metaclass=LoggerSingletonMeta):
    def __init__(self):
        self.Session = local_session

    def log(self, level, message):
        entry = LogEntry(level=level, message=message)
        session = self.Session()
        session.add(entry)
        session.commit()
        session.refresh(entry)


logger = Logger()
