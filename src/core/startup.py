from src.core.database import local_session


class StartupManager:
    """
    Manager for registering and running startup methods.

    The `StartupManager` allows you to register methods that need to be executed during the application startup.
    These methods can perform various initialization tasks.

    Args:
        None

    Attributes:
        startup_methods (list): A list to store registered startup methods.

    Methods:
        register(method): Register a method as a startup method.
        run(session): Run all registered startup methods with the provided session.

    Example usage:

    ```python
    startup_manager = StartupManager()

    @startup_manager.register
    async def my_startup_method(session):
        # Initialization logic here

    async def startup_event():
        with local_session() as session:
            await startup_manager.run(session)
    ```

    """

    def __init__(self):
        self.startup_methods = []

    async def register(self, method):
        """
        Register a method as a startup method.

        Args:
            method (callable): The method to be registered as a startup method.

        Returns:
            callable: The same method that was registered.

        Example usage:

        ```python
        @startup_manager.register
        async def my_startup_method(session):
            # Initialization logic here
        ```

        """
        self.startup_methods.append(method)
        return method

    async def run(self, session):
        """
        Run all registered startup methods with the provided session.

        Args:
            session: The database session that can be passed to startup methods.
        """
        for method in self.startup_methods:
            method(session)


startup_manager = StartupManager()


async def startup_event():
    """
    Event handler for running startup methods.

    This function is called during the application startup to execute all registered startup methods.
    """

    with local_session() as session:
        await startup_manager.run(session)
