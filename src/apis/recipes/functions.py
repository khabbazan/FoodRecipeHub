
from src.helpers.response import Response
from src.resources.recipes import Recipe
from src.resources.recipes import Tag
from src.helpers.messages import get_message

async def create(user, recipe_data, request, db_session, *args, **kwargs):

    recipe = await Recipe().create(user, recipe_data, db_session)
    if recipe:
        msg = get_message("create_recipe", **{"user": user.phone_number, "title": recipe_data.title})
    else:
        msg = get_message("failed_create_recipe", **{"user": user.phone_number, "title": recipe_data.title})

    return Response(message=msg, request=request, json_kwargs={"Recipe UUID": recipe.uuid})

async def update(user, recipe_edit, request, db_session, *args, **kwargs):

    if await Recipe().update(user, recipe_edit, db_session):
        msg = get_message("update_recipe", **{"user": user.phone_number, "uuid": recipe_edit.uuid})
    else:
        msg = get_message("failed_update_recipe", **{"user": user.phone_number, "uuid": recipe_edit.uuid})

    return Response(message=msg, request=request)

async def delete(user, recipe_uuid, request, db_session, *args, **kwargs):

    if await Recipe().delete(user, recipe_uuid, db_session):
        msg = get_message("delete_recipe", **{"user": user.phone_number, "uuid": recipe_uuid})
    else:
        msg = get_message("failed_delete_recipe", **{"user": user.phone_number, "uuid": recipe_uuid})

    return Response(message=msg, request=request)


async def show_all(search, filter, page, request, db_session, *args, **kwargs):

    recipes = await Recipe().show_all(search, filter, page, db_session)

    return Response(message=recipes, request=request, query_message=True)


async def show_detail(recipe_uuid, request, db_session, *args, **kwargs):

    recipe = await Recipe().show_detail(recipe_uuid, db_session)

    return Response(message=recipe, request=request, query_message=True)


async def show_tags(page, request, db_session, *args, **kwargs):

    tags = await Tag().show_all(page, db_session)

    return Response(message=tags, request=request, query_message=True)
