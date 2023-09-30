from fastapi import status
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from fastapi_babel.core import make_gettext as _


class BadRequestException(Exception):
    """
    Exception for representing a Bad Request error.

    Args:
        message (str): The error message.
        status_code (int): The HTTP status code for the error (default 400 Bad Request).

    Attributes:
        message (str): The error message.
        status_code (int): The HTTP status code for the error.
        error_type (str): The type of the error.

    Example usage:

    ```python
    raise BadRequestException("Invalid input data")
    ```
    """

    def __init__(self, message="Bad Request", status_code=status.HTTP_400_BAD_REQUEST):
        self.message = _(message)
        self.status_code = status_code
        self.error_type = "Bad Request Exception"
        super().__init__(self.message)


class CredentialException(Exception):
    """
    Exception for representing a Credential Error (e.g., Invalid Credentials).

    Args:
        message (str): The error message.
        status_code (int): The HTTP status code for the error (default 401 Unauthorized).

    Attributes:
        message (str): The error message.
        status_code (int): The HTTP status code for the error.
        error_type (str): The type of the error.

    Example usage:

    ```python
    raise CredentialException("Invalid username or password")
    ```
    """

    def __init__(self, message="Invalid Credentials", status_code=status.HTTP_401_UNAUTHORIZED):
        self.message = _(message)
        self.status_code = status_code
        self.error_type = "Credential Exception"
        super().__init__(self.message)


def handle_credential_exception(request: Request, exc: CredentialException) -> JSONResponse:
    """
    Handle CredentialException and return a JSONResponse.

    Args:
        request (Request): The incoming request object.
        exc (CredentialException): The CredentialException instance.

    Returns:
        JSONResponse: A JSON response containing error details.
    """
    return JSONResponse(status_code=exc.status_code, content={"msg": exc.message, "type": exc.error_type})


def handle_bad_request_exception(request: Request, exc: BadRequestException) -> JSONResponse:
    """
    Handle BadRequestException and return a JSONResponse.

    Args:
        request (Request): The incoming request object.
        exc (BadRequestException): The BadRequestException instance.

    Returns:
        JSONResponse: A JSON response containing error details.
    """
    return JSONResponse(status_code=exc.status_code, content={"msg": exc.message, "type": exc.error_type})


def handle_value_error_exception(request: Request, exc: ValueError) -> JSONResponse:
    """
    Handle ValueError exception and return a JSONResponse with error details.

    Args:
        request (Request): The incoming request object.
        exc (ValueError): The ValueError instance.

    Returns:
        JSONResponse: A JSON response containing error details.
    """
    error_details = []
    if hasattr(exc, "errors"):
        for error in exc.errors():
            loc = list(error["loc"])
            msg = error["msg"]
            error_type = error["type"]

            error_details.append({"loc": loc, "msg": msg, "type": error_type})
    else:
        error_details.append({"msg": str(exc), "type": "Value Error"})

    return JSONResponse(status_code=400, content={"detail": error_details})


def handle_rate_limit_exception(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Handle RateLimitExceeded exception and return a JSONResponse with error details.

    Args:
        request (Request): The incoming request object.
        exc (RateLimitExceeded): The RateLimitExceeded instance.

    Returns:
        Response: A JSON response containing rate limit exceeded error details.
    """
    response = JSONResponse({"error": f"Rate limit exceeded: {exc.detail}"}, status_code=429)
    response = request.app.state.limiter._inject_headers(response, request.state.view_rate_limit)
    return response
