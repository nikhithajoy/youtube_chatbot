from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Dict

from app.ingestion.youtube_client import YouTubeClient
from app.ingestion.channel_service import ChannelService
from app.core.logger import get_logger

router = APIRouter(prefix="/channel", tags=["Channel"])
logger = get_logger(__name__)


class ChannelIngestRequest(BaseModel):
    channel_url: HttpUrl
    
class ChannelIngestResponse(BaseModel):
    channel_id: str
    total_videos: int
    

@router.post("/", response_model=ChannelIngestResponse)
async def ingest_channel(request: ChannelIngestRequest):
    try:
        youtube_client = YouTubeClient()
        channel_service = ChannelService(youtube_client)
        result = channel_service.ingest_channel(str(request.channel_url))

        return ChannelIngestResponse(
            channel_id=result["channel_id"],
            total_videos=result["total_videos"],
        )
    except Exception as e:
        logger.error(f"Error ingesting channel: {e}")
        raise HTTPException(status_code=500, detail="Failed to ingest channel")