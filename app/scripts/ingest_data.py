import json
import sys
from pathlib import Path

from app.youtube.fetcher import YouTubeVideoFetcher

# Add root path to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))  # two levels up


if __name__ == "__main__":
    video_urls = [
        "https://youtu.be/RGaW82k4dK4?si=HLF8xj-IckgVTDbq"
    ]

    fetcher = YouTubeVideoFetcher()
    all_data = []

    for url in video_urls:
        video_data = fetcher.fetch_video_data(url)
        if video_data:
            all_data.append(video_data.model_dump(mode="json"))

    # Ensure data folder exists
    Path("data").mkdir(parents=True, exist_ok=True)

    with open("data/metadata.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"[Success] Successfully fetched and saved {len(all_data)} videos.")
