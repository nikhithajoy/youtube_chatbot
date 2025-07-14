import json
from app.youtube.fetcher import YouTubeVideoFetcher
from app.database.models import YouTubeVideo
from app.database.session import SessionLocal, engine, Base

if __name__ == "__main__":
    video_urls = [
        "https://www.youtube.com/watch?v=aircAruvnKk",
        "https://www.youtube.com/watch?v=Ew7fOQpkKBw"
    ]

    fetcher = YouTubeVideoFetcher()
    db = SessionLocal()

    for url in video_urls:
        video_data = fetcher.fetch_video_data(url)
        if video_data:
            # Check if already exists
            exists = db.query(YouTubeVideo).filter_by(id=video_data.video_id).first()
            if exists:
                print(f"[SKIP] {video_data.video_id} already in DB")
                continue

            video = YouTubeVideo(
                id=video_data.video_id,
                title=video_data.title,
                description=video_data.description,
                duration_sec=video_data.duration_sec,
                transcription=video_data.transcription,
                url=video_data.url
            )

            db.add(video)

    db.commit()
    db.close()

    print(f"All videos ingested into DB.")
