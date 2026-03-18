from youtube_transcript_api import YouTubeTranscriptApi
import asyncio
import os

from app.core.logger import get_logger
from app.db.repository import VideoRepository
from app.db.base import get_database
from app.transcription.audio_downloader import download_audio
from app.transcription.speech_to_text import generate_transcript

logger = get_logger(__name__)


class TranscriptService:
    def __init__(self, video_repository: VideoRepository | None = None):

        if video_repository is None:
            db = get_database()
            self.video_repository = VideoRepository(db)
        else:
            self.video_repository = video_repository

    async def ingest_transcript(self, video_id: str):
        audio_path = None

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
            logger.info(f"Transcript not available for video {video_id}, running fallback speech-to-text")
            audio_path = await asyncio.to_thread(download_audio, video_id)
            try:
                text = await asyncio.to_thread(generate_transcript, audio_path)
                await self.video_repository.update_video_transcript(video_id, text)
                logger.info(f"Fallback transcript stored for video {video_id}")
                return text
            finally:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    logger.debug(f"Deleted audio file {audio_path}")