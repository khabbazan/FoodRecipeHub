from pydantic import BaseModel
from pydantic import Field


class JWTTokenSchema(BaseModel):
    """
    JWTTokenSchema represents the structure of a JWT (JSON Web Token) token.

    This Pydantic model defines the structure of a JWT token, including its access token, refresh token, and token type.

    Attributes:
        access_token (str): The JWT access token.
            This token is used for authenticating and authorizing requests.
        refresh_token (str): The JWT refresh token.
            This token is used for obtaining new access tokens when they expire.
        token_type (str): The type of token (e.g., "JWT").
            This indicates the type of token being used for authentication.

    Example usage:

    ```python
    token = JWTTokenSchema(
        access_token="access_token_value",
        refresh_token="refresh_token_value",
        token_type="JWT"
    )
    ```

    Fields:
        access_token (str): The JWT access token.
        refresh_token (str): The JWT refresh token.
        token_type (str): The type of token.

    """

    access_token: str = Field(description="The JWT access token.")
    refresh_token: str = Field(description="The JWT refresh token.")
    token_type: str = Field(description="The type of token (e.g., 'JWT').")
