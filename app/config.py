import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = str(os.environ.get("REDIS_HOST"))
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT"))
    MONGO_HOST: str = str(os.environ.get("MONGO_HOST"))
    MONGO_PORT: int = int(os.environ.get("MONGO_PORT"))
    MONGO_USER: str = str(os.environ.get("MONGO_USER"))
    MONGO_PASSWORD: str = str(os.environ.get("MONGO_PASSWORD"))
    MONGO_DB: str = str(os.environ.get("MONGO_DB", "image_processing_db"))
    MONGO_COLLECTION: str = str(os.environ.get("MONGO_COLLECTION", "requests"))
    MONGO_URL: str = (
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
    )
    CELERY_BROKER_URL: str = str(os.environ.get("CELERY_BROKER_URL"))
    CELERY_RESULT_BACKEND: str = str(os.environ.get("CELERY_RESULT_BACKEND"))
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    COMPRESSED_IMAGE_MINIO_BUCKET: str = "compressed-images"
    ORIGINAL_IMAGE_MINIO_BUCKET: str = "original-images"
    MINIO_HOST: str = str(os.environ.get("MINIO_HOST"))
    MINIO_PORT: int = int(os.environ.get("MINIO_PORT"))
    MINIO_ROOT_USER: str = str(os.environ.get("MINIO_ROOT_USER"))
    MINIO_ROOT_PASSWORD: str = str(os.environ.get("MINIO_ROOT_PASSWORD"))
    MINIO_SECURE: bool = bool(os.environ.get("MINIO_SECURE", False))
    MINIO_URL: str = f"{MINIO_HOST}:{MINIO_PORT}"


@lru_cache(maxsize=128, typed=True)
def get_settings():
    return Settings()
