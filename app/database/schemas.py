from pydantic import BaseModel, HttpUrl
from typing import Optional

class VideoData(BaseModel):
    video_id: str
    title: str
    description: Optional[str] = None
    duration_sec: Optional[int] = None
    transcription: Optional[str] = None
    url: HttpUrl