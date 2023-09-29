from src.helpers.response import Response
from src.resources.users import User
from src.helpers.messages import get_message


async def login_create(user_data, request, db_session, *args, **kwargs):

    tokens = await User().login_create(user_data, db_session)

    if tokens:
        msg = get_message("login_user", **{"user": user_data.phone_number})
    else:
        msg = get_message("failed_login_user", **{"user": user_data.phone_number})

    return Response(message=msg, json_kwargs=tokens, request=request)


async def update(user, data, request, db_session, *args, **kwargs):

    if await User().update(user, data, db_session):
        msg = get_message("update_user", **{"user": user.phone_number})
    else:
        msg = get_message("update_login_user", **{"user": user.phone_number})

    return Response(message=msg, request=request)


async def show_all(search, filter, page, request, db_session, *args, **kwargs):

    users = await User().show_all(search, filter, page, db_session)

    return Response(message=users, request=request, query_message=True)


async def show_detail(user, request, db_session, *args, **kwargs):

    user_detail = await User().show_detail(user, db_session)

    return Response(message=user_detail, request=request, query_message=True)


async def logout(user, request, db_session, *args, **kwargs):

    if await User().logout(user, db_session):
        msg = get_message("logout_user", **{"user": user.phone_number})
    else:
        msg = get_message("failed_logout_user", **{"user": user.phone_number})

    return Response(message=msg, request=request)


async def refresh(user, refresh_token, request, db_session, *args, **kwargs):

    tokens = await User().refresh(user, refresh_token, db_session)

    if tokens:
        msg = get_message("refresh_token", **{"user": user.phone_number})
    else:
        msg = get_message("failed_refresh_token", **{"user": user.phone_number})

    return Response(message=msg, json_kwargs=tokens, request=request)
