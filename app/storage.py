from io import BytesIO

from minio import Minio

from app.config import get_settings

settings = get_settings()


async def get_minio_client() -> Minio:
    return Minio(
        endpoint=settings.MINIO_URL,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=settings.MINIO_SECURE,
    )


async def upload_to_minio(bucket_name: str, object_name: str, data: bytes) -> str:
    client = await get_minio_client()
    client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=BytesIO(data),
        length=len(data),
    )
    return client.presigned_get_object(
        bucket_name=bucket_name,
        object_name=object_name,
    )
