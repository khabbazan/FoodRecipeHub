from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.ratelimiter import recipes_rate_limit_depends
from src.helpers.response.schemas import Page, ResponseQuery, ResponseSchema, ResponseListQuery
from src.core.database import get_db_session
from src.helpers.jwt.oauth2 import get_current_user
from src.resources.recipes.schemas import RecipeSchema, RecipeEditSchema, RecipeFilterSchema
from src.apis.recipes.functions import (
    create as create_function,
    update as update_function,
    delete as delete_function,
    show_all as show_all_function,
    show_detail as show_detail_function,
    show_tags as show_tags_function,
)

router = APIRouter(
    prefix="/recipe",
    tags=["Recipe"],
    responses={404: {"detail": "Not found"}},
    dependencies=[Depends(recipes_rate_limit_depends)],
)


@router.post("/create", response_model=ResponseSchema, description="Create a new recipe.")
async def create_recipe(
    recipe_data: RecipeSchema = Depends(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:
    """
    Create a new recipe.

    Args:
        recipe_data (RecipeSchema): The recipe data to create.
        current_user (str): The current user.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseSchema: The response containing the created recipe.
    """
    response = await create_function(current_user, recipe_data, None, db_session)
    return response.get()


@router.post("/update", response_model=ResponseSchema, description="Update an existing recipe.")
async def update_recipe(
    recipe_edit: RecipeEditSchema = Depends(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:
    """
    Update an existing recipe.

    Args:
        recipe_edit (RecipeEditSchema): The edited recipe data.
        current_user (str): The current user.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseSchema: The response containing the updated recipe.
    """
    response = await update_function(current_user, recipe_edit, None, db_session)
    return response.get()


@router.post("/delete", response_model=ResponseSchema, description="Delete a recipe.")
async def delete_recipe(
    recipe_uuid: str = Query(..., description="The UUID of the recipe to delete."),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:
    """
    Delete a recipe.

    Args:
        recipe_uuid (str): The UUID of the recipe to delete.
        current_user (str): The current user.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseSchema: The response indicating the success of the deletion.
    """
    response = await delete_function(current_user, recipe_uuid, None, db_session)
    return response.get()


@router.get("/list", response_model=ResponseListQuery, description="Get a list of recipes.")
async def list_recipes(
    search: Optional[str] = None,
    filter: RecipeFilterSchema = Depends(),
    page: Page = Depends(),
    db_session: Session = Depends(get_db_session),
) -> ResponseListQuery:
    """
    Get a list of recipes.

    Args:
        search (Optional[str]): Optional search query.
        filter (RecipeFilterSchema): Filtering criteria.
        page (Page): Pagination information.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseListQuery: The response containing a list of recipes.
    """
    response = await show_all_function(search, filter, page, None, db_session)
    return response.get()


@router.get("/detail", response_model=ResponseQuery, description="Get details of a specific recipe.")
async def get_recipe_detail(
    recipe_uuid: str = Query(..., description="The UUID of the recipe to fetch details for."),
    db_session: Session = Depends(get_db_session),
) -> ResponseQuery:
    """
    Get details of a specific recipe.

    Args:
        recipe_uuid (str): The UUID of the recipe to fetch details for.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseQuery: The response containing the recipe details.
    """
    response = await show_detail_function(recipe_uuid, None, db_session)
    return response.get()


@router.get("/tags", response_model=ResponseQuery, description="Get a list of recipe tags.")
async def get_recipe_tags(
    page: Page = Depends(),
    db_session: Session = Depends(get_db_session),
) -> ResponseQuery:
    """
    Get a list of recipe tags.

    Args:
        page (Page): Pagination information.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseQuery: The response containing a list of recipe tags.
    """
    response = await show_tags_function(page, None, db_session)
    return response.get()
