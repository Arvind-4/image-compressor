from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from app.config import get_settings

settings = get_settings()


async def get_collection(
    db_name: str = settings.MONGO_DB,
    collection_name: str = settings.MONGO_COLLECTION,
) -> AsyncIOMotorCollection:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URL)
    db: AsyncIOMotorDatabase = client[db_name]
    collection: AsyncIOMotorCollection = db[collection_name]
    return collection
