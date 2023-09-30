from src.helpers.response import Response
from src.helpers.messages import get_message
from src.resources.relations import Relation


async def follow(user, following_phone_number, request, db_session, *args, **kwargs):
    """
    Follow another user.

    Args:
        user (User): The user initiating the follow action.
        following_phone_number (str): The phone number of the user to follow.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the result of the follow action.
    """
    if await Relation().follow(user, following_phone_number, db_session):
        msg = get_message("follow_user", **{"user": user.phone_number, "following": following_phone_number})
    else:
        msg = get_message("failed_follow_user", **{"user": user.phone_number, "following": following_phone_number})

    return Response(message=msg, request=request)


async def unfollow(user, following_phone_number, request, db_session, *args, **kwargs):
    """
    Unfollow another user.

    Args:
        user (User): The user initiating the unfollow action.
        following_phone_number (str): The phone number of the user to unfollow.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the result of the unfollow action.
    """
    if await Relation().unfollow(user, following_phone_number, db_session):
        msg = get_message("unfollow_user", **{"user": user.phone_number, "following": following_phone_number})
    else:
        msg = get_message("failed_unfollow_user", **{"user": user.phone_number, "following": following_phone_number})

    return Response(message=msg, request=request)


async def follower_list(user, page, request, db_session, *args, **kwargs):
    """
    Get a list of followers for a user.

    Args:
        user (User): The user for whom to retrieve followers.
        page (int): The page number.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the list of followers.
    """
    followers = await Relation().follower_list(user, page, db_session)

    return Response(message=followers, request=request, query_message=True)


async def following_list(user, page, request, db_session, *args, **kwargs):
    """
    Get a list of users that the specified user is following.

    Args:
        user (User): The user for whom to retrieve the list of following users.
        page (int): The page number.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the list of following users.
    """
    following = await Relation().following_list(user, page, db_session)

    return Response(message=following, request=request, query_message=True)
