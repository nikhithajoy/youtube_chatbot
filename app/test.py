import sys
from pathlib import Path

# Allow running this test either from the repository root (recommended) or
# from the `app/` directory. If running from inside `app/`, ensure the
# project root is on sys.path so the `app` package can be imported.
if Path.cwd().name == "app":
	sys.path.insert(0, str(Path.cwd().parent))

import asyncio
from app.ingestion.youtube_client import YouTubeClient
from app.ingestion.channel_service import ChannelService
from app.db.repository import ChannelRepository, VideoRepository
from app.db.base import connect_to_mongo, close_mongo_connection, get_database


async def run():
    await connect_to_mongo()
    db = get_database()
    
    channel_repo = ChannelRepository(db)
    video_repo = VideoRepository(db)
    client = YouTubeClient()
    channel_service = ChannelService(client, channel_repo, video_repo)
    channel_url = "https://www.youtube.com/@freecodecamp"
    result = await channel_service.ingest_channel(channel_url)
    print(result)
 
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(run())