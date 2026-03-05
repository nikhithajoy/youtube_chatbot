from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.ingestion.youtube_client import YouTubeClient
from app.ingestion.channel_service import ChannelService
from app.db.base import get_database
from app.db.repository import ChannelRepository, VideoRepository
from app.core.logger import get_logger

router = APIRouter(prefix="/channel", tags=["Channel"])
logger = get_logger(__name__)


class ChannelRequest(BaseModel):
    channel_url: HttpUrl
    
@router.post("/")
async def ingest_channel(request: ChannelRequest):
    try:
        logger.info(f"Received channel ingestion request for URL: {request.channel_url}")

        # Build dependencies
        db = get_database()
        channel_repo = ChannelRepository(db)
        video_repo = VideoRepository(db)

        youtube_client = YouTubeClient()
        service = ChannelService(youtube_client, channel_repo, video_repo)

        result = await service.ingest_channel(str(request.channel_url))

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error ingesting channel: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to ingest channel"
        )