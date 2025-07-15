from app.youtube.fetcher import YouTubeVideoFetcher
from app.database.models import YouTubeVideo, YouTubeChannel
from app.database.session import SessionLocal
from yt_dlp import YoutubeDL


def get_channel_videos(channel_url: str):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
        'skip_download': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        entries = info.get("entries", [])
        return entries, info


if __name__ == "__main__":
    channel_url = input("Paste YouTube channel link: ").strip()

    video_fetcher = YouTubeVideoFetcher()
    db = SessionLocal()

    videos_data, channel_info = get_channel_videos(channel_url)
    channel_id = channel_info.get("id")

    # Check if channel already exists
    existing_channel = db.query(YouTubeChannel).filter_by(id=channel_id).first()
    if not existing_channel:
        new_channel = YouTubeChannel(
            id=channel_id,
            title=channel_info.get("title"),
            description=channel_info.get("description"),
            url=channel_url
        )
        db.add(new_channel)
        db.commit()
        print(f"Added new channel: {new_channel.title}")
    else:
        new_channel = existing_channel
        print(f"Channel already exists: {new_channel.title}")

    # Process each video
    for entry in videos_data:
        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
        existing_video = db.query(YouTubeVideo).filter_by(id=entry["id"]).first()
        if existing_video:
            print(f"[SKIP] {entry['id']} already exists.")
            continue

        video_data = video_fetcher.fetch_video_data(video_url)
        if not video_data:
            continue

        video = YouTubeVideo(
            id=video_data.video_id,
            title=video_data.title,
            description=video_data.description,
            duration_sec=video_data.duration_sec,
            transcription=video_data.transcription,
            url=str(video_data.url),
            channel_id=new_channel.id
        )
        db.add(video)
        print(f"[+Video] {video.title}")

    db.commit()
    db.close()
    print(f"All channel videos saved to database.")
