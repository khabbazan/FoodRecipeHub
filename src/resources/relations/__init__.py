
from sqlalchemy.orm import load_only

from src.helpers.cache.decorators import cache
from src.helpers.cache.decorators import expire_cache

from src.core.exceptions import BadRequestException
from src.resources.users.models import UserModel
from src.resources.relations.models import RelationModel
from src.resources.users.schemas import UserQuerySchemaSimple
from fastapi_babel.core import make_gettext as _

class Relation:

    async def follow(self, user, following_phone_number, db_session):

        users_phone_numbers_query = db_session.query(UserModel).filter(
            UserModel.id.in_(following.following_id for following in user.following)
        ).options(load_only("phone_number"))

        if following_phone_number not in users_phone_numbers_query.all():
            raise BadRequestException(message=_("The requested following not find"))

        following_user = db_session.query(UserModel).filter(UserModel.phone_number == following_phone_number).first()
        return await self._follow(user=user, following_user=following_user, session=db_session)


    @staticmethod
    @expire_cache(cache_keys=["user_follower_list", "user_following_list"])
    async def _follow(user, following_user, session):

        relation = RelationModel(
            follower_id=user.id,
            following_id=following_user.id
        )

        session.add(relation)
        session.commit()

        return relation


    async def unfollow(self, user, following_phone_number, db_session):

        following_phone_numbers_query = db_session.query(UserModel).filter(
            UserModel.id.in_(following.following_id for following in user.following)
        ).options(load_only("phone_number"))

        if following_phone_number not in following_phone_numbers_query.all():
            raise BadRequestException(message=_("The requested following does not followed to the authenticated user"))

        following_user = db_session.query(UserModel).filter(UserModel.phone_number == following_phone_number).first()
        return await self._unfollow(user=user, following_user=following_user, session=db_session)


    @staticmethod
    @expire_cache(cache_keys=["user_follower_list", "user_following_list"])
    async def _unfollow(user, following_user, session):

        result = session.query(RelationModel).filter(
            RelationModel.follower_id == user.id, RelationModel.following_id == following_user.id
        ).delete()

        session.commit()

        return result


    async def follower_list(self, user, page, db_session):

        return await self._follower_list(user=user, page=page, session=db_session)


    @staticmethod
    @cache(cache_key="user_follower_list")
    async def _follower_list(user, page, session):

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

        return await self._following_list(user=user, page=page, session=db_session)


    @staticmethod
    @cache(cache_key="user_following_list")
    async def _following_list(user, page, session):

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
