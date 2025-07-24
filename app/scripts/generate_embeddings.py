from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")
embedder = Embedder()
vector_store = VectorStore(DATABASE_URL)

from sqlalchemy.orm import sessionmaker
from app.database.models import YouTubeVideo  # assuming you have a model Video

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

videos = session.query(YouTubeVideo).all()

for video in videos:
    content = f"{video.title}\n{video.summary}\n{video.transcript}"
    vector = embedder.embed_text(content)
    vector_store.update_video_embedding(video.id, vector)
