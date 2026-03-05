import sys
from pathlib import Path

# Allow running this test either from the repository root (recommended) or
# from the `app/` directory. If running from inside `app/`, ensure the
# project root is on sys.path so the `app` package can be imported.
if Path.cwd().name == "app":
	sys.path.insert(0, str(Path.cwd().parent))

from app.ingestion.youtube_client import YouTubeClient
from app.ingestion.channel_service import ChannelService


def run():
	client = YouTubeClient()
	channel_service = ChannelService(client)

	channel_url = "https://www.youtube.com/@freecodecamp"
	result = channel_service.ingest_channel(channel_url)
	print(result)


if __name__ == "__main__":
	run()