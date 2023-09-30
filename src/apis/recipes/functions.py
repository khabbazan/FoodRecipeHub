from src.helpers.response import Response
from src.resources.recipes import Recipe
from src.resources.recipes import Tag
from src.helpers.messages import get_message


async def create(user, recipe_data, request, db_session, *args, **kwargs):
    """
    Create a new recipe.

    Args:
        user (User): The user creating the recipe.
        recipe_data (dict): The data for the new recipe.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the result of the operation.
    """
    recipe = await Recipe().create(user, recipe_data, db_session)
    if recipe:
        msg = get_message("create_recipe", **{"user": user.phone_number, "title": recipe_data.title})
    else:
        msg = get_message("failed_create_recipe", **{"user": user.phone_number, "title": recipe_data.title})

    return Response(message=msg, request=request, json_kwargs={"Recipe UUID": recipe.uuid})


async def update(user, recipe_edit, request, db_session, *args, **kwargs):
    """
    Update an existing recipe.

    Args:
        user (User): The user updating the recipe.
        recipe_edit (dict): The data for updating the recipe.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the result of the operation.
    """
    if await Recipe().update(user, recipe_edit, db_session):
        msg = get_message("update_recipe", **{"user": user.phone_number, "uuid": recipe_edit.uuid})
    else:
        msg = get_message("failed_update_recipe", **{"user": user.phone_number, "uuid": recipe_edit.uuid})

    return Response(message=msg, request=request)


async def delete(user, recipe_uuid, request, db_session, *args, **kwargs):
    """
    Delete a recipe.

    Args:
        user (User): The user deleting the recipe.
        recipe_uuid (str): The UUID of the recipe to be deleted.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the result of the operation.
    """
    if await Recipe().delete(user, recipe_uuid, db_session):
        msg = get_message("delete_recipe", **{"user": user.phone_number, "uuid": recipe_uuid})
    else:
        msg = get_message("failed_delete_recipe", **{"user": user.phone_number, "uuid": recipe_uuid})

    return Response(message=msg, request=request)


async def show_all(search, filter, page, request, db_session, *args, **kwargs):
    """
    Show a list of recipes.

    Args:
        search (str): The search criteria.
        filter (str): The filter criteria.
        page (int): The page number.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the list of recipes.
    """
    recipes = await Recipe().show_all(search, filter, page, db_session)

    return Response(message=recipes, request=request, query_message=True)


async def show_detail(recipe_uuid, request, db_session, *args, **kwargs):
    """
    Show detailed information about a recipe.

    Args:
        recipe_uuid (str): The UUID of the recipe to be displayed.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the detailed information of the recipe.
    """
    recipe = await Recipe().show_detail(recipe_uuid, db_session)

    return Response(message=recipe, request=request, query_message=True)


async def show_tags(page, request, db_session, *args, **kwargs):
    """
    Show a list of tags.

    Args:
        page (int): The page number.
        request (Request): The incoming request object.
        db_session: The database session.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        Response: A Response object containing the list of tags.
    """
    tags = await Tag().show_all(page, db_session)

    return Response(message=tags, request=request, query_message=True)
