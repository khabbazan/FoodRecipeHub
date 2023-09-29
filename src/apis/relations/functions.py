from src.helpers.response import Response
from src.helpers.messages import get_message

from src.resources.relations import Relation


async def follow(user, following_phone_number, request, db_session, *args, **kwargs):

    if await Relation().follow(user, following_phone_number, db_session):
        msg = get_message("follow_user", **{"user": user.phone_number, "following": following_phone_number})
    else:
        msg = get_message("failed_follow_user", **{"user": user.phone_number, "following": following_phone_number})

    return Response(message=msg, request=request)


async def unfollow(user, following_phone_number, request, db_session, *args, **kwargs):

    if await Relation().unfollow(user, following_phone_number, db_session):
        msg = get_message("unfollow_user", **{"user": user.phone_number, "following": following_phone_number})
    else:
        msg = get_message("failed_unfollow_user", **{"user": user.phone_number, "following": following_phone_number})

    return Response(message=msg, request=request)


async def follower_list(user, page, request, db_session, *args, **kwargs):

    followers = await Relation().follower_list(user, page, db_session)

    return Response(message=followers, request=request, query_message=True)


async def following_list(user, page, request, db_session, *args, **kwargs):

    following = await Relation().following_list(user, page, db_session)

    return Response(message=following, request=request, query_message=True)
