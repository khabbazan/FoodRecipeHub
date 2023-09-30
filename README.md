# Food Recipe Hub FastAPI Project

The Food Recipe Hub is a FastAPI project that provides RESTful APIs for sharing food recipes and allows users to follow others. This project aims to make it easy for food enthusiasts to create, share, and discover delicious recipes.

## APIs

### User
- `POST /user/login`: Create a new user session.
- `POST /user/update`: Update user information.
- `GET /user/list`: Get a list of all users.
- `GET /user/detail`: Get detailed information about a user.
- `GET /user/logout`: Log out the user.
- `GET /user/refreshToken`: Refresh the user's authentication token.

### Recipe
- `POST /recipe/create`: Create a new recipe.
- `POST /recipe/update`: Update an existing recipe.
- `POST /recipe/delete`: Delete a recipe.
- `GET /recipe/list`: List all recipes.
- `GET /recipe/detail`: Get detailed information about a recipe.
- `GET /recipe/tags`: Get recipe tags.

### Relation
- `POST /relation/follow`: Follow another user.
- `POST /relation/unfollow`: Unfollow a user.
- `GET /relation/follower_list`: Get the list of followers for a user.
- `GET /relation/following_list`: Get the list of users a user is following.

## Project Features

- **Rate Limiting:** The project implements rate limiting settings to control API usage.

- **Image Handling:** It handles images through an S3 object server.

- **Redis Cache System:** Results are cached using Redis, with cache expiration for related apis to improve performance.

- **Load Testing:** There's a load testing scenario included using Locust in the test directory to evaluate API performance under load.

- **Multilingual Support:** The project supports translation in different languages to make it accessible to a wider audience.

## Setup and Installation

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Configure your project settings and database connection in `src/core/settings`.
4. Run the development server with `python main.py`.

## Configuration (When Debug Mode is Turned Off)

### PostgreSQL Configuration

If running in production mode, configure your PostgreSQL database connection in the project's settings file.

```python
_DB_USER = ""
_DB_PASSWORD = ""
_DB_HOST = ""
_DB_PORT = ""
_DB_NAME = ""

DATABASE = {
    "URL": f"sqlite:///.//db.sqlite3" if DEBUG else f"postgresql+psycopg2://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}",
    "PARAMS": {"connect_args": {"check_same_thread": False}} if DEBUG else {"isolation_level": "REPEATABLE READ"},
}
```

### Rate Limiting
Set rate limiting configurations for different parts of the project.

```python
RATE_LIMIT = {
    "default_limits": ["200 per day", "50 per hour"],
    "router_limits": {"recipes": "10 per hour"},
}
```

### Redis Cache
Configure Redis cache settings.

```python
CACHE = {
    "PREFIX": "cache:",
    "HOST_IP": "localhost",
    "HOST_PORT": "6379",
    "DB_NUM": "0",
    "DEFAULT_EXPIRE_TIME": 3600,
}
```

### S3 Object Server (Image Handling)
Configure S3 settings for handling images and static files.

```python
S3_CONFIGS = {
    "service_name": "s3",
    "aws_access_key_id": "",
    "aws_secret_access_key": "",
    "aws_storage_bucket_name": "",
    "aws_s3_region_name": None,
    "aws_s3_custom_domain": "",
    "aws_s3_endpoint_url": "",
    "aws_s3_file_overwrite": True,
    "aws_default_acl": "public-read",
    "aws_s3_object_parameters": {
        "cachecontrol": "max-age=86400",
    },
}
```

## Project Documentation

You can find Entity-Relationship (ER) diagrams in the `documents` directory. These diagrams have been generated using [eralchemy2](https://github.com/maurerle/eralchemy2) to help you understand the project's database schema.

## Testing

You can run the load test scenario using Locust by following the instructions in the `tests` directory.

## Contributors

- [Alireza Khabbazan](https://github.com/khabbazan)

## License

This project is open for contributions, and contributions are welcome from the community. It is licensed under the terms of MIT. Feel free to fork, contribute, and make this project even better!
