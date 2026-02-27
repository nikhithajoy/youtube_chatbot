from typing import List, Dict, Optional
from urllib.parse import urlparse
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.core.config import get_settings
from app.core.logger import get_logger


settings = get_settings()
logger = get_logger(__name__)


class YouTubeClient:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        
        
    def extract_channel_id(self, url: str) -> Optional[str]:
        """
        Extract Channel ID
            """
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/")
            
        if path.startswith("channel/"):
            return path.split("/")[1]
            
        if path.startswith("@"):
            return path
            
        return path.split("/")[1] if "/" in path else path
            
    def resolve_channel_id(self, identifier: str) -> str:
        """
        Convert custom name to canonical channel ID
        """
        try:
            if identifier.startswith("@"):
                response = self.youtube.search().list(
                    part="snippet",
                    q=identifier,
                    type="channel",
                    maxResults=1,
                ).execute()
                    
                return response["items"][0]["snippet"]["channelId"]
                
            # If already looks like a channel ID
            if identifier.startswith("UC"):
                return identifier
                
            # Custom URL fallback
            response = self.youtube.search().list(
                part="snippet",
                q=identifier,
                type="channel",
                maxResults=1,
            ).execute()
                
            return response["items"][0]["snippet"]["channelId"]
        except HttpError as e:
            logger.error(f"Failed to extract channel ID from URL '{url}': {e}")
            raise
        
    def get_uploads_playlist_id(self, channel_id: str) -> str:
        """
        Get the playlist ID that contains all uploads for a channel
        """
        try:
            response = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id,
            ).execute()
                
            return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        except HttpError as e:
            logger.error(f"Failed to get uploads playlist ID for channel '{channel_id}': {e}")
            raise
        
    def fetch_all_videos(self, uploads_playlist_id: str) -> List[Dict]:
        """
        Fetch all videos with metadata
        """
        
        videos = []
        next_page_token: Optional[str] = None
        
        try:
            while True:
                response = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token,
                ).execute()
                    
                for item in response["items"]:
                    video_id = item["contentDetails"]["videoId"]
                    videos.append(
                        {
                            "video_id": video_id,
                            "title": item["snippet"]["title"],
                            "description": item["snippet"]["description"],
                            "published_at": item["contentDetails"]["videoPublishedAt"],
                        }
                    )
                    
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            logger.info(f"Fetched {len(videos)} videos from playlist '{uploads_playlist_id}'")
            return videos
        except HttpError as e:
            logger.error(f"Failed to fetch videos from playlist '{uploads_playlist_id}': {e}")
            raise
            
    