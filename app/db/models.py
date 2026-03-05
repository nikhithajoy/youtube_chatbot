from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Channel(BaseModel):
    channel_id: str = Field(..., description="YouTube channel ID")
    channel_name: str = Field(..., description="YouTube channel name")
    channel_url: str = Field(..., description="YouTube channel URL")
    videos_count: int = Field(..., description="Total number of videos in the channel")
    
class Video(BaseModel):
    video_id: str = Field(..., description="YouTube video ID")
    channel_id: str = Field(..., description="ID of the channel this video belongs to")
    title: str = Field(..., description="Video title")
    description: Optional[str] = Field(None, description="Video description")
    published_at: datetime = Field(..., description="Video publish date and time")
    transcript: str = Field(default="Pending", description="Video transcript text")