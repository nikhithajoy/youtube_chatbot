from typing import Dict, List

from app.db.models import Channel, Video
from datetime import datetime
from app.db.repository import ChannelRepository, VideoRepository
from app.ingestion.youtube_client import YouTubeClient
from app.core.logger import get_logger

logger = get_logger(__name__)

class ChannelService:
    """
    Orchastrates full channel ingestion workflow using YouTubeClient and other components.
    
    Responsibilities:
    - Parse channel URL
    - Resolve channel ID
    - Retrieve uploads playlist
    - Fetch video metadata
    """
    
    def __init__(self, 
                 youtube_client: YouTubeClient, 
                 channel_repository: ChannelRepository, 
                 video_repository: VideoRepository):
        self.youtube_client = youtube_client
        self.channel_repository = channel_repository
        self.video_repository = video_repository

    async def ingest_channel(self, channel_url: str) -> List[Dict]:
        if not isinstance(channel_url, str):
                channel_url = str(channel_url)

        logger.info(f"Starting ingestion for channel URL: {channel_url}")
            
        # Extract channel identifier from URL
        identifier = self.youtube_client.extract_channel_id(channel_url)
        logger.debug(f"Extracted channel identifier: {identifier}")
            
        # Resolve to canonical channel ID
        channel_id = self.youtube_client.resolve_channel_id(identifier)
        logger.debug(f"Resolved channel ID: {channel_id}")
        
        # Check if channel already exists in database
        exists = await self.channel_repository.channel_exists(channel_id)
        if exists:
            logger.info("Channel already exists in database, skipping ingestion")
        
        # Fetch uploads playlist
        uploads_playlist_id = self.youtube_client.get_uploads_playlist_id(channel_id)
        logger.info(f"Retrieved uploads playlist ID: {uploads_playlist_id}")

        # Fetch video metadata
        videos_data = self.youtube_client.fetch_all_videos(uploads_playlist_id)
        logger.info(f"Fetched {len(videos_data)} videos for channel {channel_id}")

        # Store channel (use identifier as a fallback name)
        channel_model = Channel(
            channel_id=channel_id,
            channel_name=identifier,
            channel_url=channel_url,
            videos_count=len(videos_data),
        )   
        if not exists:
            await self.channel_repository.create_channel(channel_model)
            logger.info(f"Channel {channel_id} created in database")     
        
        # Convert videos to models
        videos_models: List[Video] = []
        for video in videos_data:
            videos_models.append(
                Video(
                    video_id=video["video_id"],
                    channel_id=channel_id,
                    title=video["title"],
                    description=video.get("description"),
                    published_at=datetime.fromisoformat(
                        video["published_at"].replace("Z", "+00:00")
                    ),
                )
            )
            
        # Store videos
        await self.video_repository.insert_video(videos_models)
        logger.info(f"Inserted {len(videos_models)} videos into database for channel {channel_id}")
        
        return {
            "channel_id": channel_id,
            "total_videos": len(videos_data)
        }