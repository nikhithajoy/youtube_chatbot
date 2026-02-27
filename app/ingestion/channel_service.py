from typing import Dict, List

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
    
    def __init__(self, youtube_client: YouTubeClient):
        self.youtube_client = youtube_client
        
    def ingest_channel(self, channel_url: str) -> List[Dict]:
        if not isinstance(channel_url, str):
                channel_url = str(channel_url)

        logger.info(f"Starting ingestion for channel URL: {channel_url}")
            
        # Step 1: Extract channel identifier from URL
        identifier = self.youtube_client.extract_channel_id(channel_url)
        logger.debug(f"Extracted channel identifier: {identifier}")
            
        # Step 2: Resolve to canonical channel ID
        channel_id = self.youtube_client.resolve_channel_id(identifier)
        logger.debug(f"Resolved channel ID: {channel_id}")

        # Step 3: Get uploads playlist ID
        uploads_playlist_id = self.youtube_client.get_uploads_playlist_id(channel_id)
        logger.debug(f"Retrieved uploads playlist ID: {uploads_playlist_id}")

        # Step 4: Fetch video metadata
        videos = self.youtube_client.fetch_all_videos(uploads_playlist_id)
        logger.debug(f"Fetched video metadata: {videos}")

        return {
            "channel_id": channel_id,
            "total_videos": len(videos),
            "videos": videos,
        }