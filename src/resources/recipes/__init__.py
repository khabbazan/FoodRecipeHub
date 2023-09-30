from src.helpers.cache.decorators import cache
from src.helpers.cache.decorators import expire_cache

from src.core.exceptions import BadRequestException
from src.resources.recipes.models import TagModel
from src.resources.recipes.models import RecipeModel
from src.resources.recipes.schemas import TagQuerySchema
from src.resources.recipes.schemas import RecipeQuerySchema
from src.resources.recipes.schemas import RecipeQuerySchemaSimple
from src.resources.users.schemas import UserQuerySchemaSimple
from fastapi_babel.core import make_gettext as _


class Recipe:
    """
    Operations related to Recipe management.

    Class Methods:
    - create(user, recipe_data, db_session): Create a new recipe.
    - update(user, data, db_session): Update a recipe.
    - delete(user, recipe_uuid, db_session): Delete a recipe.
    - show_all(search, filter, page, db_session): Retrieve a list of recipes based on search and filter criteria.
    - show_detail(recipe_uuid, db_session): Retrieve details of a specific recipe.
    """

    async def create(self, user, recipe_data, db_session):
        """
        Create a new recipe.

        Args:
            user (UserModel): The user creating the recipe.
            recipe_data (RecipeCreateSchema): Data for creating the recipe.
            db_session (Session): SQLAlchemy session.

        Returns:
            RecipeModel: The created recipe.
        """
        return await self._create(user=user, recipe_data=recipe_data, session=db_session)

    @staticmethod
    @expire_cache(cache_keys=["recipe_list", "recipe_detail", "user_list", "user_detail"])
    async def _create(user, recipe_data, session):
        """
        Internal method to create a recipe.

        Args:
            user (UserModel): The user creating the recipe.
            recipe_data (RecipeCreateSchema): Data for creating the recipe.
            session (Session): SQLAlchemy session.

        Returns:
            RecipeModel: The created recipe.
        """
        recipe = RecipeModel(
            title=recipe_data.title,
            content=recipe_data.content,
            is_active=recipe_data.is_active,
            tags=[TagModel(title=tag) for tag in recipe_data.tags],
            user_id=user.id,
        )

        session.add(recipe)
        session.commit()

        return recipe

    async def update(self, user, data, db_session):
        """
        Update a recipe.

        Args:
            user (UserModel): The user updating the recipe.
            data (RecipeUpdateSchema): Data for updating the recipe.
            db_session (Session): SQLAlchemy session.

        Returns:
            bool: True if the recipe was successfully updated.

        Raises:
            BadRequestException: If the requested recipe does not belong to the authenticated user.
        """
        user_recipes = user.recipes
        if data.uuid not in [recipe.uuid for recipe in user_recipes]:
            raise BadRequestException(message=_("The requested recipe does not belong to the authenticated user"))

        trim_data = {key: value for key, value in data.model_dump().items() if value is not None and value != ""}

        return await self._update(user=user, data=trim_data, session=db_session)

    @staticmethod
    @expire_cache(cache_keys=["recipe_list", "recipe_detail", "user_list", "user_detail"])
    async def _update(user, data, session) -> bool:
        """
        Internal method to update a recipe.

        Args:
            user (UserModel): The user updating the recipe.
            data (dict): Data for updating the recipe.
            session (Session): SQLAlchemy session.

        Returns:
            bool: True if the recipe was successfully updated.
        """
        data_tags = data.pop("tags", None)
        instance_query = session.query(RecipeModel).filter(RecipeModel.uuid == data.get("uuid"))
        instance_query.update(values=data)

        if data_tags is not None:
            recipe = instance_query.first()
            recipe.tags = [TagModel(title=tag) for tag in data_tags]

        session.commit()

        return instance_query

    async def delete(self, user, recipe_uuid, db_session):
        """
        Delete a recipe.

        Args:
            user (UserModel): The user deleting the recipe.
            recipe_uuid (str): The UUID of the recipe to delete.
            db_session (Session): SQLAlchemy session.

        Returns:
            bool: True if the recipe was successfully deleted.

        Raises:
            BadRequestException: If the requested recipe does not belong to the authenticated user.
        """
        user_recipes = user.recipes
        if recipe_uuid not in [recipe.uuid for recipe in user_recipes]:
            raise BadRequestException(message=_("The requested recipe does not belong to the authenticated user"))

        return await self._delete(user=user, uuid=recipe_uuid, session=db_session)

    @staticmethod
    @expire_cache(cache_keys=["recipe_list", "recipe_detail", "user_list", "user_detail"])
    async def _delete(user, uuid, session) -> bool:
        """
        Internal method to delete a recipe.

        Args:
            user (UserModel): The user deleting the recipe.
            uuid (str): The UUID of the recipe to delete.
            session (Session): SQLAlchemy session.

        Returns:
            bool: True if the recipe was successfully deleted.
        """
        session.query(RecipeModel).filter(RecipeModel.uuid == uuid).delete()
        session.commit()

        return True

    async def show_all(self, search, filter, page, db_session):
        """
        Retrieve a list of recipes based on search and filter criteria.

        Args:
            search (str): Search query.
            filter (RecipeFilterSchema): Filtering criteria.
            page (PaginationQuerySchema): Pagination settings.
            db_session (Session): SQLAlchemy session.

        Returns:
            dict: Dictionary containing a list of recipes, page count, and total count.
        """
        trim_filter_param = {key: value for key, value in filter.model_dump().items() if value is not None and value != ""}

        return await self._show_all(search=search, filter=trim_filter_param, page=page, session=db_session)

    @staticmethod
    @cache(cache_key="recipe_list")
    async def _show_all(search, filter, page, session):
        """
        Internal method to retrieve a list of recipes based on search and filter criteria.

        Args:
            search (str): Search query.
            filter (dict): Filtering criteria.
            page (PaginationQuerySchema): Pagination settings.
            session (Session): SQLAlchemy session.

        Returns:
            dict: Dictionary containing a list of recipes, page count, and total count.
        """
        query = RecipeModel.search(session, query_string=search)

        for key, value in filter.items():
            query = query.filter(getattr(RecipeModel, key) == value)

        total_items = query.count()
        recipes = query.offset((page.page_number - 1) * page.page_size).limit(page.page_size).all()

        recipe_flatten_query = [
            RecipeQuerySchemaSimple(
                uuid=recipe.uuid,
                title=recipe.title,
                user=UserQuerySchemaSimple(phone_number=recipe.user.phone_number, email=recipe.user.email),
            ).model_dump()
            for recipe in recipes
        ]

        return {
            "data": recipe_flatten_query,
            "page_count": (total_items + page.page_size - 1) // page.page_size,
            "count": total_items,
        }

    async def show_detail(self, recipe_uuid, db_session):
        """
        Retrieve details of a specific recipe.

        Args:
            recipe_uuid (str): The UUID of the recipe to retrieve.
            db_session (Session): SQLAlchemy session.

        Returns:
            dict: Dictionary containing the details of the recipe.
        """
        return await self._show_detail(recipe_uuid=recipe_uuid, session=db_session)

    @staticmethod
    @cache(cache_key="recipe_detail")
    async def _show_detail(recipe_uuid, session):
        """
        Internal method to retrieve details of a specific recipe.

        Args:
            recipe_uuid (str): The UUID of the recipe to retrieve.
            session (Session): SQLAlchemy session.

        Returns:
            dict: Dictionary containing the details of the recipe.
        """
        recipe = session.query(RecipeModel).filter(RecipeModel.uuid == recipe_uuid).first()
        recipe_flatten = {}

        if recipe:
            recipe_flatten = RecipeQuerySchema(
                uuid=recipe.uuid,
                title=recipe.title,
                content=recipe.content,
                is_active=recipe.is_active,
                tags=[TagQuerySchema(title=tag.title.name, display_title=_(tag.title.value)) for tag in recipe.tags],
                user=UserQuerySchemaSimple(phone_number=recipe.user.phone_number, email=recipe.user.email),
                created_at=recipe.created_at,
            ).model_dump()

        return {
            "data": recipe_flatten,
        }


class Tag:
    """
    Operations related to Tag management.

    Class Methods:
    - show_all(page, db_session): Retrieve a list of tags.
    """

    async def show_all(self, page, db_session):
        """
        Retrieve a list of tags.

        Args:
            page (PaginationQuerySchema): Pagination settings.
            db_session (Session): SQLAlchemy session.

        Returns:
            dict: Dictionary containing a list of tags, page count, and total count.
        """
        return await self._show_all(page=page, session=db_session)

    @staticmethod
    @cache(cache_key="tag_list")
    async def _show_all(page, session):
        """
        Internal method to retrieve a list of tags.

        Args:
            page (PaginationQuerySchema): Pagination settings.
            session (Session): SQLAlchemy session.

        Returns:
            dict: Dictionary containing a list of tags, page count, and total count.
        """
        query = session.query(TagModel.title)

        total_items = query.count()
        tags = query.offset((page.page_number - 1) * page.page_size).limit(page.page_size).all()

        tag_flatten_query = [
            TagQuerySchema(
                title=tag.title.name,
                display_title=_(tag.title.value),
            ).model_dump()
            for tag in tags
        ]

        return {
            "data": tag_flatten_query,
            "page_count": (total_items + page.page_size - 1) // page.page_size,
            "count": total_items,
        }
