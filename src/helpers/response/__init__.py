import copy
from colorama import Fore, Style

from src.helpers.response.schemas import ResponseQuery
from src.helpers.response.schemas import ResponseSchema
from src.helpers.response.schemas import ResponseListQuery
from src.helpers.response.schemas import ResponseWithTokenSchema
from src.helpers.logger.models import LogLevel
from src.helpers.logger import logger


class Response:
    """
    Response is a utility class for constructing API responses.

    This class helps in creating structured API responses by combining message, error, and additional data.
    It also logs the response and allows printing it to the console with color-coded indicators.

    Args:
        message (str, optional): The main message to include in the response.
        request (str, optional): The request context associated with the response.
        error (str, optional): An error message to include in the response.
        json_kwargs (dict, optional): Additional JSON data to include in the response.
        query_message (bool, optional): Indicates if the response is for a query operation.
        print_console (bool, optional): Indicates whether to print the response to the console.

    Methods:
        get(): Get the constructed response as a specific response schema based on the provided data.

    Example usage:

    ```python
    response = Response(message="Success", json_kwargs={"data": {"key": "value"}})
    result = response.get()
    ```

    In this example, the `Response` class is used to construct a response with a message and additional data.
    The `get()` method is then called to obtain the response in the desired schema format.

    """

    def __init__(
        self,
        message=None,
        request=None,
        error=None,
        json_kwargs=None,
        query_message=False,
        print_console=True,
    ):

        self.request = request
        self.query_message = query_message
        self.print_console = print_console
        self.json_kwargs = dict(json_kwargs) if json_kwargs else {}

        ############# populate function `message`, `error` and `data` to json_kwargs #############
        if "message" not in self.json_kwargs:
            self.json_kwargs["message"] = message

        if "error" not in self.json_kwargs:
            self.json_kwargs["error"] = error

    def get(self):
        """
        Get the constructed response as a specific response schema.

        Returns:
            ResponseQuery or ResponseSchema or ResponseListQuery or ResponseWithTokenSchema:
                The constructed response as an instance of a specific response schema.

        Example usage:

        ```python
        response = Response(message="Success", json_kwargs={"data": {"key": "value"}})
        result = response.get()
        ```

        """

        kwargs = copy.deepcopy(self.json_kwargs)
        response = {k: v for k, v in kwargs.items() if v is not None}

        if self.print_console:
            print(
                f"{Fore.LIGHTRED_EX}ERROR:\t" if "error" in response.keys() else f"{Fore.LIGHTGREEN_EX}INFO:\t",
                f"{response.get('error','')}{response.get('message','')}",
                Style.RESET_ALL,
            )

        logger.log(
            level=LogLevel.ERROR if "error" in response.keys() else LogLevel.INFO,
            message=response,
        )

        if self.query_message:
            message = response.pop("message")
            if "page_count" not in message.keys():
                return ResponseQuery(
                    data=message["data"],
                )
            else:
                return ResponseListQuery(data=message["data"], page_count=message["page_count"], count=message["count"])

        elif "access_token" in response.keys():
            return ResponseWithTokenSchema(
                message=response.pop("message"),
                access_token=response.pop("access_token"),
                refresh_token=response.pop("refresh_token"),
                token_type=response.pop("token_type"),
                metadata=None if not response else {**response},
            )
        else:
            return ResponseSchema(
                message=f'{response.pop("message","")}{response.pop("error","")}',
                metadata=None if not response else {**response},
            )
