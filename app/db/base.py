from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from app.core.config import get_settings
from app.core.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorClient] = None

mongodb = MongoDB()

async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    mongodb.client = AsyncIOMotorClient(settings.DATABASE_URL)
    mongodb.database = mongodb.client.get_default_database()
    logger.info("Connected to MongoDB")
    
async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    # Motor client objects do not implement truth-value testing. Compare
    # explicitly with None to avoid "Database objects do not implement
    # truth value testing" runtime errors.
    if mongodb.client is not None:
        mongodb.client.close()
    logger.info("MongoDB connection closed")
    
def get_database() -> AsyncIOMotorClient:
    # Motor database objects don't support bool(), so check against None.
    if mongodb.database is None:
        raise Exception("Database connection is not established")
    return mongodb.database