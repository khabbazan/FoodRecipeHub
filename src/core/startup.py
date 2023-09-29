
from src.core.databse import local_session

class StartupManager:
    def __init__(self):
        self.startup_methods = []

    async def register(self, method):
        self.startup_methods.append(method)
        return method

    async def run(self, session):
        for method in self.startup_methods:
            method(session)

startup_manager = StartupManager()

async def startup_event():

    with local_session() as session:
        await startup_manager.run(session)
