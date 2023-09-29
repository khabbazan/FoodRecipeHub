from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status
from fastapi import Query
from sqlalchemy.orm import Session

from src.helpers.response.schemas import Page
from src.helpers.response.schemas import ResponseQuery
from src.helpers.response.schemas import ResponseSchema
from src.helpers.response.schemas import ResponseListQuery

from src.core.databse import get_db_session
from src.helpers.jwt.oauth2 import get_current_user
from src.resources.recipes.schemas import RecipeSchema
from src.resources.recipes.schemas import RecipeEditSchema
from src.resources.recipes.schemas import RecipeFilterSchema

from src.apis.recipes.functions import create as create_function
from src.apis.recipes.functions import update as update_function
from src.apis.recipes.functions import delete as delete_function
from src.apis.recipes.functions import show_all as show_all_function
from src.apis.recipes.functions import show_detail as show_detail_function
from src.apis.recipes.functions import show_tags as show_tags_function

from src.core.ratelimiter import recipes_rate_limit_depends

router = APIRouter(prefix="/recipe", tags=["Recipe"], responses={404: {"detail": "Not found"}}, dependencies=[Depends(recipes_rate_limit_depends)])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema)
async def create(
    request: Request,
    recipe_data: RecipeSchema = Depends(RecipeSchema),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:

    response = await create_function(current_user, recipe_data, request, db_session)
    return response.get()


@router.post("/update", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseSchema)
async def update(
    request: Request,
    recipe_edit: RecipeEditSchema = Depends(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:

    response = await update_function(current_user, recipe_edit, request, db_session)
    return response.get()


@router.post("/delete", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseSchema)
async def delete(
    request: Request,
    recipe_uuid: str = Query(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:

    response = await delete_function(current_user, recipe_uuid, request, db_session)
    return response.get()


@router.get("/list", status_code=status.HTTP_200_OK, response_model=ResponseListQuery)
async def show_all(
    request: Request,
    search: Optional[str] = Query(None),
    filter: RecipeFilterSchema = Depends(RecipeFilterSchema),
    page: Page = Depends(Page),
    db_session: Session = Depends(get_db_session),
) -> ResponseListQuery:

    response = await show_all_function(search, filter, page, request, db_session)
    return response.get()


@router.get("/detail", status_code=status.HTTP_200_OK, response_model=ResponseQuery)
async def show_detail(
    request: Request,
    recipe_uuid: str = Query(),
    db_session: Session = Depends(get_db_session),
) -> ResponseQuery:

    response = await show_detail_function(recipe_uuid, request, db_session)
    return response.get()


@router.get("/tags", status_code=status.HTTP_200_OK, response_model=ResponseQuery)
async def show_tags(
    request: Request,
    page: Page = Depends(Page),
    db_session: Session = Depends(get_db_session),
) -> ResponseQuery:

    response = await show_tags_function(page, request, db_session)
    return response.get()
