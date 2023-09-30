from sqlalchemy.orm import load_only

from src.helpers.cache.decorators import cache
from src.helpers.cache.decorators import expire_cache

from src.core.exceptions import BadRequestException
from src.resources.users.models import UserModel
from src.resources.relations.models import RelationModel
from src.resources.users.schemas import UserQuerySchemaSimple
from fastapi_babel.core import make_gettext as _


class Relation:
    """
    Represents a class for managing user relationships.

    This class provides methods to follow and unfollow users, retrieve follower and following lists, and handle user relationships.

    Methods:
        follow: Follow a user.
        _follow: Internal method to perform the follow operation.
        unfollow: Unfollow a user.
        _unfollow: Internal method to perform the unfollow operation.
        follower_list: Get the list of followers.
        _follower_list: Internal method to retrieve the list of followers.
        following_list: Get the list of users being followed.
        _following_list: Internal method to retrieve the list of users being followed.

    """

    async def follow(self, user, following_phone_number, db_session):
        """
        Follow a user.

        Args:
            user (UserModel): The authenticated user.
            following_phone_number (str): The phone number of the user to follow.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            RelationModel: The relationship object representing the follow action.
        """
        users_phone_numbers_query = (
            db_session.query(UserModel).filter(UserModel.id.in_(following.following_id for following in user.following)).options(load_only("phone_number"))
        )

        if following_phone_number not in users_phone_numbers_query.all():
            raise BadRequestException(message=_("The requested following not found"))

        following_user = db_session.query(UserModel).filter(UserModel.phone_number == following_phone_number).first()
        return await self._follow(user=user, following_user=following_user, session=db_session)

    @staticmethod
    @expire_cache(cache_keys=["user_follower_list", "user_following_list"])
    async def _follow(user, following_user, session):
        """
        Internal method to perform the follow operation.

        Args:
            user (UserModel): The authenticated user.
            following_user (UserModel): The user to follow.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            RelationModel: The relationship object representing the follow action.
        """
        relation = RelationModel(follower_id=user.id, following_id=following_user.id)

        session.add(relation)
        session.commit()

        return relation

    async def unfollow(self, user, following_phone_number, db_session):
        """
        Unfollow a user.

        Args:
            user (UserModel): The authenticated user.
            following_phone_number (str): The phone number of the user to unfollow.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            int: The number of relationships deleted (0 or 1).
        """
        following_phone_numbers_query = (
            db_session.query(UserModel).filter(UserModel.id.in_(following.following_id for following in user.following)).options(load_only("phone_number"))
        )

        if following_phone_number not in following_phone_numbers_query.all():
            raise BadRequestException(message=_("The requested following does not follow the authenticated user"))

        following_user = db_session.query(UserModel).filter(UserModel.phone_number == following_phone_number).first()
        return await self._unfollow(user=user, following_user=following_user, session=db_session)

    @staticmethod
    @expire_cache(cache_keys=["user_follower_list", "user_following_list"])
    async def _unfollow(user, following_user, session):
        """
        Internal method to perform the unfollow operation.

        Args:
            user (UserModel): The authenticated user.
            following_user (UserModel): The user to unfollow.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            int: The number of relationships deleted (0 or 1).
        """
        result = session.query(RelationModel).filter(RelationModel.follower_id == user.id, RelationModel.following_id == following_user.id).delete()

        session.commit()

        return result

    async def follower_list(self, user, page, db_session):
        """
        Get the list of followers for the authenticated user.

        Args:
            user (UserModel): The authenticated user.
            page (Page): Pagination information.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing the list of followers, page count, and total count.
        """
        return await self._follower_list(user=user, page=page, session=db_session)

    @staticmethod
    @cache(cache_key="user_follower_list")
    async def _follower_list(user, page, session):
        """
        Internal method to retrieve the list of followers for a user.

        Args:
            user (UserModel): The user for whom to retrieve followers.
            page (Page): Pagination information.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing the list of followers, page count, and total count.
        """
        query = session.query(UserModel).filter(UserModel.id.in_(follower.follower_id for follower in user.followers))

        total_items = query.count()
        followers = query.offset((page.page_number - 1) * page.page_size).limit(page.page_size).all()

        followers_flatten_query = [
            UserQuerySchemaSimple(
                phone_number=user.phone_number,
                email=user.email,
            ).model_dump()
            for user in followers
        ]

        return {
            "data": followers_flatten_query,
            "page_count": (total_items + page.page_size - 1) // page.page_size,
            "count": total_items,
        }

    async def following_list(self, user, page, db_session):
        """
        Get the list of users being followed by the authenticated user.

        Args:
            user (UserModel): The authenticated user.
            page (Page): Pagination information.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing the list of users being followed, page count, and total count.
        """
        return await self._following_list(user=user, page=page, session=db_session)

    @staticmethod
    @cache(cache_key="user_following_list")
    async def _following_list(user, page, session):
        """
        Internal method to retrieve the list of users being followed by a user.

        Args:
            user (UserModel): The user for whom to retrieve the list of users being followed.
            page (Page): Pagination information.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing the list of users being followed, page count, and total count.
        """
        query = session.query(UserModel).filter(UserModel.id.in_(following.following_id for following in user.following))

        total_items = query.count()
        following = query.offset((page.page_number - 1) * page.page_size).limit(page.page_size).all()

        following_flatten_query = [
            UserQuerySchemaSimple(
                phone_number=user.phone_number,
                email=user.email,
            ).model_dump()
            for user in following
        ]

        return {
            "data": following_flatten_query,
            "page_count": (total_items + page.page_size - 1) // page.page_size,
            "count": total_items,
        }
