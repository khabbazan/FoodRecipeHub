from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from src.helpers.response.schemas import Page, ResponseQuery, ResponseSchema, ResponseListQuery, ResponseWithTokenSchema
from src.core.database import get_db_session
from src.helpers.jwt.oauth2 import get_current_user
from src.resources.users.schemas import UserEditSchema, UserLoginForm, UserFilterSchema
from src.apis.users.functions import (
    login_create as login_create_function,
    logout as logout_function,
    refresh as refresh_function,
    update as update_function,
    show_all as show_all_function,
    show_detail as show_detail_function,
)


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"detail": "Not found"}},
)


@router.post(
    "/login",
    response_model=ResponseWithTokenSchema | ResponseSchema,
    description="Create a user login session.",
)
async def login_create(
    request: Request,
    form_data: UserLoginForm = Depends(),
    db_session: Session = Depends(get_db_session),
) -> ResponseWithTokenSchema | ResponseSchema:
    """
    Create a user login session.

    Args:
        request (Request): The incoming HTTP request.
        form_data (UserLoginForm): The user login form data.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        Union[ResponseWithTokenSchema, ResponseSchema]: The response containing the result of the login session creation.
    """
    response = await login_create_function(form_data.to_schema(), request, db_session)
    return response.get()


@router.post(
    "/update",
    response_model=ResponseSchema,
    description="Update user information.",
)
async def update(
    request: Request,
    edit_data: UserEditSchema = Depends(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:
    """
    Update user information.

    Args:
        request (Request): The incoming HTTP request.
        edit_data (UserEditSchema): The user data to update.
        current_user (str): The current user's phone number.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseSchema: The response containing the result of the user update.
    """
    response = await update_function(current_user, edit_data, request, db_session)
    return response.get()


@router.get(
    "/list",
    response_model=ResponseListQuery,
    description="Get a list of users.",
)
async def show_all(
    request: Request,
    search: Optional[str] = Query(None),
    filter: UserFilterSchema = Depends(UserFilterSchema),
    page: Page = Depends(Page),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseListQuery:
    """
    Get a list of users.

    Args:
        request (Request): The incoming HTTP request.
        search (Optional[str]): Optional search query.
        filter (UserFilterSchema): Filtering criteria.
        page (Page): Pagination information.
        current_user (str): The current user's phone number.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseListQuery: The response containing a list of users.
    """
    response = await show_all_function(search, filter, page, request, db_session)
    return response.get()


@router.get(
    "/detail",
    response_model=ResponseQuery,
    description="Get details of the current user.",
)
async def show_detail(
    request: Request,
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseQuery:
    """
    Get details of the current user.

    Args:
        request (Request): The incoming HTTP request.
        current_user (str): The current user's phone number.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseQuery: The response containing the user details.
    """
    response = await show_detail_function(current_user, request, db_session)
    return response.get()


@router.get(
    "/logout",
    response_model=ResponseSchema,
    description="Logout the current user.",
)
async def logout(
    request: Request,
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:
    """
    Logout the current user.

    Args:
        request (Request): The incoming HTTP request.
        current_user (str): The current user's phone number.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseSchema: The response containing the result of the logout operation.
    """
    response = await logout_function(current_user, request, db_session)
    return response.get()


@router.get(
    "/refreshToken",
    response_model=ResponseWithTokenSchema,
    description="Refresh user authentication tokens.",
)
async def refresh(
    request: Request,
    refresh_token: str = Query(),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseWithTokenSchema:
    """
    Refresh user authentication tokens.

    Args:
        request (Request): The incoming HTTP request.
        refresh_token (str): The refresh token.
        current_user (str): The current user's phone number.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseWithTokenSchema: The response containing the refreshed tokens.
    """
    response = await refresh_function(current_user, refresh_token, request, db_session)
    return response.get()
