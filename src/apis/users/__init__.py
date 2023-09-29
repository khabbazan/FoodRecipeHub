from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status
from fastapi import Query
from sqlalchemy.orm import Session

from src.helpers.response.schemas import ResponseQuery
from src.helpers.response.schemas import ResponseSchema
from src.helpers.response.schemas import ResponseListQuery
from src.helpers.response.schemas import Page
from src.helpers.response.schemas import ResponseWithTokenSchema

from src.core.databse import get_db_session
from src.helpers.jwt.oauth2 import get_current_user
from src.resources.users.schemas import UserEditSchema
from src.resources.users.schemas import UserLoginForm
from src.resources.users.schemas import UserFilterSchema

from src.apis.users.functions import login_create as login_create_function
from src.apis.users.functions import logout as logout_function
from src.apis.users.functions import refresh as refresh_function
from src.apis.users.functions import update as update_function
from src.apis.users.functions import show_all as show_all_function
from src.apis.users.functions import show_detail as show_detail_function


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"detail": "Not found"}},
)


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=ResponseWithTokenSchema | ResponseSchema)
async def login_create(
    request: Request,
    form_data: UserLoginForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    response = await login_create_function(form_data.to_schema(), request, db_session)
    return response.get()


@router.post("/update", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseSchema)
async def update(
    request: Request,
    edit_data: UserEditSchema = Depends(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
):
    response = await update_function(current_user, edit_data, request, db_session)
    return response.get()


@router.get("/list", status_code=status.HTTP_200_OK, response_model=ResponseListQuery)
async def show_all(
    request: Request,
    search: Optional[str] = Query(None),
    filter: UserFilterSchema = Depends(UserFilterSchema),
    page: Page = Depends(Page),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
):
    response = await show_all_function(search, filter, page, request, db_session)
    return response.get()


@router.get("/detail", status_code=status.HTTP_200_OK, response_model=ResponseQuery)
async def show_detail(
    request: Request,
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
):
    response = await show_detail_function(current_user, request, db_session)
    return response.get()


@router.get("/logout", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
async def logout(
    request: Request,
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
):
    response = await logout_function(current_user, request, db_session)
    return response.get()


@router.get("/refreshToken", status_code=status.HTTP_200_OK, response_model=ResponseWithTokenSchema)
async def refresh(
    request: Request,
    refresh_token: str = Query(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
):
    response = await refresh_function(current_user, refresh_token, request, db_session)
    return response.get()
