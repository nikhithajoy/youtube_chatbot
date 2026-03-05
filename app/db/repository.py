from typing import List
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne

from app.db.models import Channel, Video
from app.core.logger import get_logger

logger = get_logger(__name__)


class ChannelRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["channels"]

    async def channel_exists(self, channel_id: str) -> bool:
        return await self.collection.find_one({"channel_id": channel_id}) is not None

    async def create_channel(self, channel: Channel):
        result = await self.collection.insert_one(channel.dict())
        logger.info(f"Inserted channel with id {result.inserted_id}")


class VideoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["videos"]

    async def insert_video(self, videos: List[Video]) -> bool:
        operations = []

        for video in videos:
            operations.append(
                UpdateOne(
                    {"video_id": video.video_id},
                    {"$setOnInsert": video.dict()},
                    upsert=True,
                )
            )

        if operations:
            await self.collection.bulk_write(operations)

        logger.info(f"Upserted {len(videos)} videos")

    async def get_videos_by_channel(self, channel_id: str) -> List[Video]:
        cursor = self.collection.find({"channel_id": channel_id})
        videos = []
        async for doc in cursor:
            videos.append(doc)
        return videos