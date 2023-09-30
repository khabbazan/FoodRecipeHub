from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from src.helpers.response.schemas import Page, ResponseSchema, ResponseListQuery
from src.core.database import get_db_session
from src.helpers.jwt.oauth2 import get_current_user
from src.apis.relations.functions import (
    follow as follow_function,
    unfollow as unfollow_function,
    follower_list as follower_list_function,
    following_list as following_list_function,
)


router = APIRouter(
    prefix="/relation",
    tags=["Relation"],
    responses={404: {"detail": "Not found"}},
)


@router.post(
    "/follow",
    response_model=ResponseSchema,
    description="Follow another user.",
)
async def follow(
    request: Request,
    following_phone_number: str = Query(..., description="The phone number of the user to follow."),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:
    """
    Follow another user.

    Args:
        request (Request): The incoming HTTP request.
        following_phone_number (str): The phone number of the user to follow.
        current_user (str): The current user's phone number.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseSchema: The response containing the result of the follow operation.
    """
    response = await follow_function(current_user, following_phone_number, request, db_session)
    return response.get()


@router.post(
    "/unfollow",
    response_model=ResponseSchema,
    description="Unfollow another user.",
)
async def unfollow(
    request: Request,
    following_phone_number: str = Query(..., description="The phone number of the user to unfollow."),
    current_user: str = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
) -> ResponseSchema:
    """
    Unfollow another user.

    Args:
        request (Request): The incoming HTTP request.
        following_phone_number (str): The phone number of the user to unfollow.
        current_user (str): The current user's phone number.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseSchema: The response containing the result of the unfollow operation.
    """
    response = await unfollow_function(current_user, following_phone_number, request, db_session)
    return response.get()


@router.get(
    "/follower_list",
    response_model=ResponseListQuery,
    description="Get a list of followers for the current user.",
)
async def follower_list(
    request: Request,
    current_user: str = Depends(get_current_user),
    page: Page = Depends(Page),
    db_session: Session = Depends(get_db_session),
) -> ResponseListQuery:
    """
    Get a list of followers for the current user.

    Args:
        request (Request): The incoming HTTP request.
        current_user (str): The current user's phone number.
        page (Page): Pagination information.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseListQuery: The response containing a list of followers.
    """
    response = await follower_list_function(current_user, page, request, db_session)
    return response.get()


@router.get(
    "/following_list",
    response_model=ResponseListQuery,
    description="Get a list of users that the current user is following.",
)
async def following_list(
    request: Request,
    current_user: str = Depends(get_current_user),
    page: Page = Depends(Page),
    db_session: Session = Depends(get_db_session),
) -> ResponseListQuery:
    """
    Get a list of users that the current user is following.

    Args:
        request (Request): The incoming HTTP request.
        current_user (str): The current user's phone number.
        page (Page): Pagination information.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        ResponseListQuery: The response containing a list of users being followed.
    """
    response = await following_list_function(current_user, page, request, db_session)
    return response.get()
