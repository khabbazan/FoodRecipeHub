from src.helpers.response import Response
from src.resources.users import User
from src.helpers.messages import get_message


async def login_create(user_data, request, db_session, *args, **kwargs):
    """
    Create a user login session.

    Args:
        user_data (dict): User login data.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the login session result.
    """
    tokens = await User().login_create(user_data, db_session)

    if tokens:
        msg = get_message("login_user", **{"user": user_data.phone_number})
    else:
        msg = get_message("failed_login_user", **{"user": user_data.phone_number})

    return Response(message=msg, json_kwargs=tokens, request=request)


async def update(user, data, request, db_session, *args, **kwargs):
    """
    Update user information.

    Args:
        user (User): The user whose information is being updated.
        data (dict): User data to update.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the update result.
    """
    if await User().update(user, data, db_session):
        msg = get_message("update_user", **{"user": user.phone_number})
    else:
        msg = get_message("update_login_user", **{"user": user.phone_number})

    return Response(message=msg, request=request)


async def show_all(search, filter, page, request, db_session, *args, **kwargs):
    """
    Show a list of users.

    Args:
        search (str): The search criteria.
        filter (str): The filter criteria.
        page (int): The page number.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the list of users.
    """
    users = await User().show_all(search, filter, page, db_session)

    return Response(message=users, request=request, query_message=True)


async def show_detail(user, request, db_session, *args, **kwargs):
    """
    Show detailed information about a user.

    Args:
        user (User): The user whose details are being retrieved.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the detailed user information.
    """
    user_detail = await User().show_detail(user, db_session)

    return Response(message=user_detail, request=request, query_message=True)


async def logout(user, request, db_session, *args, **kwargs):
    """
    Logout a user.

    Args:
        user (User): The user to log out.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the logout result.
    """
    if await User().logout(user, db_session):
        msg = get_message("logout_user", **{"user": user.phone_number})
    else:
        msg = get_message("failed_logout_user", **{"user": user.phone_number})

    return Response(message=msg, request=request)


async def refresh(user, refresh_token, request, db_session, *args, **kwargs):
    """
    Refresh user authentication tokens.

    Args:
        user (User): The user for whom to refresh tokens.
        refresh_token (str): The refresh token used for token refresh.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the refreshed tokens or an error message.
    """
    tokens = await User().refresh(user, refresh_token, db_session)

    if tokens:
        msg = get_message("refresh_token", **{"user": user.phone_number})
    else:
        msg = get_message("failed_refresh_token", **{"user": user.phone_number})

    return Response(message=msg, json_kwargs=tokens, request=request)
