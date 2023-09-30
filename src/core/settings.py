import os
from pathlib import Path

########## General Settings  ##########
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = "0Aa298794fbb6ca2556c818166b7a9563b93f8099f6f0f4caa6cf63b88e8d3e7"

########## Uvicorn Settings  ##########
UVICORN = {
    "HOST": "127.0.0.1",
    "PORT": 9000,
}

########## Application Mode ##########
DEBUG = True

########## Docs Settings  ##########
DOCS = {
    "swagger": "/docs" if DEBUG else None,
    "redoc": "/redoc" if DEBUG else None,
}

########## Version Settings ##########
VERSION = "1.0.0"
BUILD_NUMBER = "23951e46"

########## Database Settings ##########
_DB_USER = ""
_DB_PASSWORD = ""
_DB_HOST = ""
_DB_PORT = ""
_DB_NAME = ""

DATABASE = {
    "URL": f"sqlite:///.//db.sqlite3" if DEBUG else f"postgresql+psycopg2://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}",
    "PARAMS": {"connect_args": {"check_same_thread": False}} if DEBUG else {"isolation_level": "REPEATABLE READ"},
}

########## JWT Settings ##########
JWT = {
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 60,
    "REFRESH_TOKEN_EXPIRE_MINUTES": 1440,
}

########## Ratelimit Settings ##########
RATE_LIMIT = {
    "default_limits": ["200 per day", "50 per hour"],
    "router_limits": {"recipes": "10 per hour"},
}

########## Language Settings ##########
LANGUAGE = {"default": "en", "supported": ["en", "fa"], "dir": os.path.join(BASE_DIR, "locale")}

########## Language Settings ##########
CACHE = {
    "PREFIX": "cache:",
    "HOST_IP": "localhost",
    "HOST_PORT": "6379",
    "DB_NUM": "0",
    "DEFAULT_EXPIRE_TIME": 3600,
}

########## Media Files ##########
if DEBUG:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
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

    MEDIA_URL = f"https://{S3_CONFIGS['aws_s3_custom_domain']}/"
    MEDIA_ROOT = f"https://{S3_CONFIGS['aws_s3_custom_domain']}/"
