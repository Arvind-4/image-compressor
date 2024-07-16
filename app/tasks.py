import asyncio
import time
import uuid
from typing import Any

from app.celery_app import celery
from app.config import get_settings
from app.schemas import StatusEnum
from app.services import update_status
from app.storage import upload_to_minio
from app.utils import compress_image, download_image

settings = get_settings()


@celery.task(name="process_image_task")
def process_image_task(
    request_id: str,
    objs: list[dict[str, Any]],
) -> None:
    time.sleep(5)  # Optional delay to simulate processing time
    for obj in objs:
        minio_image_urls = []
        compressed_minio_image_urls = []
        for url in obj.get("input_image_urls"):
            original_image = asyncio.run(download_image(url))
            compressed_image = asyncio.run(compress_image(original_image, 50))
            image_name = f"{uuid.uuid4()}.jpg"
            compressed_image_name = "compressed_" + image_name
            minio_image_url = asyncio.run(
                upload_to_minio(
                    bucket_name=settings.ORIGINAL_IMAGE_MINIO_BUCKET,
                    object_name=image_name,
                    data=original_image,
                ),
            )
            compressed_minio_image_url = asyncio.run(
                upload_to_minio(
                    bucket_name=settings.COMPRESSED_IMAGE_MINIO_BUCKET,
                    object_name=compressed_image_name,
                    data=compressed_image,
                ),
            )
            minio_image_urls.append(minio_image_url)
            compressed_minio_image_urls.append(compressed_minio_image_url)
        obj["input_image_urls"] = minio_image_urls
        obj["output_image_urls"] = compressed_minio_image_urls
    asyncio.run(
        update_status(
            request_id=request_id,
            status=StatusEnum.completed,
            objs=objs,
        ),
    )
