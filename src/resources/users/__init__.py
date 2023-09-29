
from src.helpers.cache.decorators import cache
from src.helpers.cache.decorators import expire_cache

from src.helpers.jwt import JWT
from src.helpers.jwt.schemas import JWTTokenSchema
from src.resources.users.models import UserModel
from src.resources.users.schemas import UserSchema
from src.resources.users.schemas import UserQuerySchema
from src.resources.users.schemas import UserQuerySchemaSimple

from src.core.exceptions import CredentialException


class User:

    async def login_create(self, user_data, db_session):

        query = db_session.query(UserModel).filter(UserModel.phone_number == user_data.phone_number)

        if query.count():
            return await self._login(find_user=query.first(), user_data=user_data, session=db_session)
        else:
            return await self._create(user_data=user_data, session=db_session)


    @staticmethod
    @expire_cache(cache_keys=["user_detail"])
    async def _login(find_user, user_data, session) -> JWTTokenSchema:
        tokens = []
        if find_user.password == user_data.password:
            find_user.is_online = True
            tokens = JWT.create_access_token(user_id=find_user.id, session=session)
        else:
            raise CredentialException()

        session.commit()

        return tokens


    @staticmethod
    @expire_cache(cache_keys=["user_list"])
    async def _create(user_data, session) -> JWTTokenSchema:

        user = UserModel(phone_number=user_data.phone_number, email=user_data.email, password=user_data.password)
        user.is_online = True
        tokens = JWT.create_access_token(user_id=user.id, session=session)

        session.add(user)
        session.commit()

        return tokens


    async def update(self, user, data, db_session):

        user_dict = {
            "username": user.phone_number,
            "email": user.email,
            "password": "",
            "gender": user.gender,
        }

        trim_dict = {key: value for key, value in data.model_dump().items() if value is not None and value != ""}

        user_dict.update(trim_dict)
        validate_schema = UserSchema.model_validate(user_dict)

        return await self._update(user=user, data=validate_schema, session=db_session)


    @staticmethod
    @expire_cache(cache_keys=["user_list", "user_detail"])
    async def _update(user, data, session) -> bool:

        data = data.model_dump()
        password = data.pop("password")
        avatar = data.pop("avatar")

        if password:
            user.password = password

        if avatar is not None:
            await user.set_avatar(name=avatar["name"], base64_image=avatar["base64_image"], session=session)


        result = session.query(UserModel).filter(UserModel.id == user.id).update(values=data)
        session.commit()

        return result

    async def show_all(self, search, filter, page, db_session):

        trim_filter_param = {key: value for key, value in filter.model_dump().items() if value is not None and value != ""}

        return await self._show_all(search=search, filter=trim_filter_param, page=page, session=db_session)


    @staticmethod
    @cache(cache_key="user_list", timeout=1000)
    async def _show_all(search, filter, page, session):

        query = UserModel.search(session, query_string=search)

        for key, val in filter.items():
            query = query.filter(getattr(UserModel, key) == val)

        total_items = query.count()
        users = query.offset((page.page_number - 1) * page.page_size).limit(page.page_size).all()

        user_flatten_query = [
            UserQuerySchemaSimple(phone_number=user.phone_number, email=user.email).model_dump()
            for user in users
        ]

        return {
            "data": user_flatten_query,
            "page_count": (total_items + page.page_size - 1) // page.page_size,
            "count": total_items,
        }


    async def show_detail(self, user, db_session):

        return await self._show_detail(user=user, session=db_session)


    @staticmethod
    @cache(cache_key="user_detail")
    async def _show_detail(user, session):

        user_flatten = UserQuerySchema(
            phone_number=user.phone_number,
            email=user.email,
            is_online=user.is_online,
            recipes=[recipe.uuid for recipe in user.recipes],
            avatars=user.get_avatars(session=session),
        ).model_dump()

        return {
            "data": user_flatten,
        }

    async def logout(self, user, db_session):

        query = db_session.query(UserModel).filter(UserModel.phone_number == user.phone_number)

        if query.count():
            return await self._logout(user=query.first(), session=db_session)
        return False


    @staticmethod
    @expire_cache(cache_keys=["user_detail"])
    async def _logout(user, session):

        user.is_online = False
        status = JWT.expire_token(user_id=user.id, session=session)

        session.commit()

        return status

    async def refresh(self, user, refresh_token, db_session):

        query = db_session.query(UserModel).filter(UserModel.phone_number == user.phone_number)

        if query.count():
            return await self._refresh(user=query.first(), refresh_token=refresh_token, session=db_session)
        return False


    @staticmethod
    async def _refresh(user, refresh_token, session):

        tokens = JWT.update_token(user_id=user.id, refresh_token=refresh_token, session=session)

        return tokens
