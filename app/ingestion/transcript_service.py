from youtube_transcript_api import YouTubeTranscriptApi
import asyncio

from app.core.logger import get_logger
from app.db.repository import VideoRepository
from app.db.base import get_database

logger = get_logger(__name__)


class TranscriptService:
    def __init__(self, video_repository: VideoRepository | None = None):

        if video_repository is None:
            db = get_database()
            self.video_repository = VideoRepository(db)
        else:
            self.video_repository = video_repository

    async def ingest_transcript(self, video_id: str):

        try:
            logger.info(f"Fetching transcript for video {video_id}")

            transcript_data = await asyncio.to_thread(
                lambda: YouTubeTranscriptApi().fetch(video_id)
            )

            transcript_text = " ".join(
                segment.text for segment in transcript_data
            )

            await self.video_repository.update_video_transcript(
                video_id,
                transcript_text
            )

            logger.info(f"Transcript stored for video {video_id}")

        except Exception as e:
            logger.warning(
                f"Transcript unavailable for video {video_id}: {str(e)}"
            )