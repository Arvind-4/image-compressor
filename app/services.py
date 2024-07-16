from datetime import datetime
from typing import Any

from bson import ObjectId

from app.db import get_collection
from app.schemas import StatusEnum


async def save_request(data):
    result = (await get_collection()).insert_one(
        {
            "status": StatusEnum.pending,
            "image_data": data,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )
    return str((await result).inserted_id)


async def update_status(
    request_id: str,
    status: str,
    objs: list[dict[str, Any]],
) -> None:
    await (await get_collection()).update_one(
        {
            "_id": ObjectId(request_id),
        },
        {
            "$set": {
                "status": status,
                "image_data": objs,
            },
        },
    )


async def fetch_request(request_id) -> dict:
    return (
        await (await get_collection()).find_one({"_id": ObjectId(request_id)}) or None
    )
