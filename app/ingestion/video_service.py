from googleapiclient.discovery import build
from app.core.config import Settings
from app.core.logger import get_logger
from app.db import repository

logger = get_logger(__name__)


class VideoService:
    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=Settings.YOUTUBE_API_KEY)
        
    async def ingest_channel_videos(self, channel_id: str):
        logger.info(f"Starting video ingestion for channel ID: {channel_id}")
        
        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            order="date",
            type="video"
        )
        
        response = request.execute()
        
        videos = []
        
        for item in response["items"]:
            video = {
                "video_id": item["id"]["videoId"],
                "channel_id": channel_id,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "published_at": item["snippet"]["publishedAt"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }
            
            videos.append(video)
            
        logger.info(f"Ingested {len(videos)} videos for channel ID: {channel_id}")
        
        for video in videos:
            await repository.insert_video(video)
        return videos