from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status
from fastapi import Query
from sqlalchemy.orm import Session

from src.helpers.response.schemas import Page
from src.helpers.response.schemas import ResponseSchema
from src.helpers.response.schemas import ResponseListQuery

from src.core.databse import get_db_session
from src.helpers.jwt.oauth2 import get_current_user

from src.apis.relations.functions import follow as follow_function
from src.apis.relations.functions import unfollow as unfollow_function
from src.apis.relations.functions import follower_list as follower_list_function
from src.apis.relations.functions import following_list as following_list_function


router = APIRouter(
    prefix="/relation",
    tags=["Relation"],
    responses={404: {"detail": "Not found"}},
)



@router.post("/follow", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema)
async def follow(
        request: Request,
        following_phone_number: str = Query(),
        current_user: str = Depends(get_current_user),
        db_session: Session = Depends(get_db_session),
):
    response = await follow_function(current_user, following_phone_number, request, db_session)
    return response.get()


@router.post("/unfollow", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseSchema)
async def unfollow(
        request: Request,
        following_phone_number: str = Query(),
        current_user: str = Depends(get_current_user),
        db_session: Session = Depends(get_db_session),
):
    response = await unfollow_function(current_user, following_phone_number, request, db_session)
    return response.get()


@router.get("/follower_list", status_code=status.HTTP_200_OK, response_model=ResponseListQuery)
async def follower_list(
        request: Request,
        current_user: str = Depends(get_current_user),
        page: Page = Depends(Page),
        db_session: Session = Depends(get_db_session),
):
    response = await follower_list_function(current_user, page, request, db_session)
    return response.get()


@router.get("/following_list", status_code=status.HTTP_200_OK, response_model=ResponseListQuery)
async def following_list(
        request: Request,
        current_user: str = Depends(get_current_user),
        page: Page = Depends(Page),
        db_session: Session = Depends(get_db_session),
):
    response = await following_list_function(current_user, page, request, db_session)
    return response.get()
