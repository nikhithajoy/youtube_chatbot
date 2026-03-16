from googleapiclient.discovery import build
from app.core.config import Settings
from app.core.logger import get_logger
from app.ingestion.transcript_service import TranscriptService
from app.db import repository
from app.db.base import get_database
from app.db.models import Video

logger = get_logger(__name__)


class VideoService:
    def __init__(self):
        self.youtube = build(
            "youtube", 
            "v3", 
            developerKey=Settings.YOUTUBE_API_KEY
        )
        
        db = get_database()
        self.video_repository = repository.VideoRepository(db)
        self.transcript_service = TranscriptService()
        
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
        
        MAX_VIDEOS = 20
        videos: list[Video] = []
        
        for item in response["items"]:
            if len(videos) >= MAX_VIDEOS:
                break
            video = {
                "video_id": item["id"]["videoId"],
                "channel_id": channel_id,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "published_at": item["snippet"]["publishedAt"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "transcript": "Pending"
            }
            
            videos.append(video)
            
        logger.info(f"Ingested {len(videos)} videos for channel ID: {channel_id}")
        
        # Bulk insert
        await self.video_repository.insert_video(videos)
        
        # Fetch transcripts asynchronously
        for video in videos:
            await self.transcript_service.ingest_transcript(video["video_id"])
            
        return videos