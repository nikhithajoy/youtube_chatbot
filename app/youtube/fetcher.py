import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional
from app.database.schemas import VideoData

class YouTubeVideoFetcher:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': False
        }

    def fetch_metadata(self, video_url: str) -> Optional[dict]:
        """Fetch metadata using yt-dlp"""

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {
                    "video_id": info.get('id'),
                    "title": info.get('title'),
                    "desc": info.get('description'),
                    "duration": info.get('duration'),
                    "url": info.get('webpage_url')
                }
        except Exception as e:
            print(f"[Error] Failed to load video metadata: {e}")
            return None
        
    def fetch_transcript(self, video_id: str) -> str:
        """Fetch transcript using YoutubeTranscriptApi."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([t['text'] for t in transcript_list])
        except Exception as e:
            print(f"Transcript fetch failed for {video_id}: {e}")
            return ""
    
    def fetch_video_data(self, video_url: str) -> Optional[VideoData]:
        """Combine metdata and transcript into a VideoData object."""
        metadata = self.fetch_metadata(video_url)

        if not metadata:
            return None
        
        transcript = self.fetch_transcript(metadata["video_id"])
        metadata["transcription"] = transcript

        try:
            return VideoData(**metadata)
        except Exception as e:
            print(f"[Error] Failed to create VideoData model: {e}")
            return None