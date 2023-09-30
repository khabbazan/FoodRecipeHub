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
    """
    Represents a class for managing user-related operations.

    This class provides methods for user login, creation, update, retrieval, logout, and token refresh.

    Methods:
        login_create: Login or create a user.
        _login: Internal method to perform login.
        _create: Internal method to create a user.
        update: Update user data.
        _update: Internal method to update user data.
        show_all: Retrieve a list of users based on search and filters.
        _show_all: Internal method to retrieve a list of users.
        show_detail: Retrieve user details.
        _show_detail: Internal method to retrieve user details.
        logout: Log out a user.
        _logout: Internal method to log out a user.
        refresh: Refresh user tokens.
        _refresh: Internal method to refresh user tokens.

    """

    async def login_create(self, user_data, db_session):
        """
        Login or create a user.

        Args:
            user_data (UserSchema): User data for login or creation.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            JWTTokenSchema: JWT tokens if login is successful, else raises CredentialException.
        """
        query = db_session.query(UserModel).filter(UserModel.phone_number == user_data.phone_number)

        if query.count():
            return await self._login(find_user=query.first(), user_data=user_data, session=db_session)
        else:
            return await self._create(user_data=user_data, session=db_session)

    @staticmethod
    @expire_cache(cache_keys=["user_detail"])
    async def _login(find_user, user_data, session) -> JWTTokenSchema:
        """
        Internal method to perform login.

        Args:
            find_user (UserModel): User object found in the database.
            user_data (UserSchema): User data for login.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            JWTTokenSchema: JWT tokens if login is successful, else raises CredentialException.
        """
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
        """
        Internal method to create a user.

        Args:
            user_data (UserSchema): User data for creation.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            JWTTokenSchema: JWT tokens upon successful user creation.
        """
        user = UserModel(phone_number=user_data.phone_number, email=user_data.email, password=user_data.password)
        user.is_online = True
        tokens = JWT.create_access_token(user_id=user.id, session=session)

        session.add(user)
        session.commit()

        return tokens

    async def update(self, user, data, db_session):
        """
        Update user data.

        Args:
            user (UserModel): The authenticated user.
            data (UserSchema): User data to update.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            bool: True if the update is successful.
        """
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
        """
        Internal method to update user data.

        Args:
            user (UserModel): The authenticated user.
            data (UserSchema): User data to update.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            bool: True if the update is successful.
        """
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
        """
        Retrieve a list of users based on search and filters.

        Args:
            search (str): The search query.
            filter (UserQuerySchemaSimple): Filter parameters.
            page (Page): Pagination information.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing the list of users, page count, and total count.
        """
        trim_filter_param = {key: value for key, value in filter.model_dump().items() if value is not None and value != ""}

        return await self._show_all(search=search, filter=trim_filter_param, page=page, session=db_session)

    @staticmethod
    @cache(cache_key="user_list", timeout=1000)
    async def _show_all(search, filter, page, session):
        """
        Internal method to retrieve a list of users based on search and filters.

        Args:
            search (str): The search query.
            filter (dict): Filter parameters.
            page (Page): Pagination information.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing the list of users, page count, and total count.
        """
        query = UserModel.search(session, query_string=search)

        for key, value in filter.items():
            query = query.filter(getattr(UserModel, key) == value)

        total_items = query.count()
        users = query.offset((page.page_number - 1) * page.page_size).limit(page.page_size).all()

        user_flatten_query = [UserQuerySchemaSimple(phone_number=user.phone_number, email=user.email).model_dump() for user in users]

        return {
            "data": user_flatten_query,
            "page_count": (total_items + page.page_size - 1) // page.page_size,
            "count": total_items,
        }

    async def show_detail(self, user, db_session):
        """
        Retrieve user details.

        Args:
            user (UserModel): The user for whom to retrieve details.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing user details.
        """
        return await self._show_detail(user=user, session=db_session)

    @staticmethod
    @cache(cache_key="user_detail")
    async def _show_detail(user, session):
        """
        Internal method to retrieve user details.

        Args:
            user (UserModel): The user for whom to retrieve details.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            dict: A dictionary containing user details.
        """
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
        """
        Log out a user.

        Args:
            user (UserModel): The user to log out.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            bool: True if logout is successful, False otherwise.
        """
        query = db_session.query(UserModel).filter(UserModel.phone_number == user.phone_number)

        if query.count():
            return await self._logout(user=query.first(), session=db_session)
        return False

    @staticmethod
    @expire_cache(cache_keys=["user_detail"])
    async def _logout(user, session):
        """
        Internal method to log out a user.

        Args:
            user (UserModel): The user to log out.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            bool: True if logout is successful, False otherwise.
        """
        user.is_online = False
        status = JWT.expire_token(user_id=user.id, session=session)

        session.commit()

        return status

    async def refresh(self, user, refresh_token, db_session):
        """
        Refresh user tokens.

        Args:
            user (UserModel): The user to refresh tokens for.
            refresh_token (str): The user's refresh token.
            db_session (Session): SQLAlchemy session for database operations.

        Returns:
            JWTTokenSchema: JWT tokens after refresh.
        """
        query = db_session.query(UserModel).filter(UserModel.phone_number == user.phone_number)

        if query.count():
            return await self._refresh(user=query.first(), refresh_token=refresh_token, session=db_session)
        return False

    @staticmethod
    async def _refresh(user, refresh_token, session):
        """
        Internal method to refresh user tokens.

        Args:
            user (UserModel): The user to refresh tokens for.
            refresh_token (str): The user's refresh token.
            session (Session): SQLAlchemy session for database operations.

        Returns:
            JWTTokenSchema: JWT tokens after refresh.
        """
        tokens = JWT.update_token(user_id=user.id, refresh_token=refresh_token, session=session)

        return tokens
