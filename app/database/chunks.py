from app.database.session import get_db
from app.database.models import Video, Chunk
from app.models.embedder import Embedder
from sqlalchemy.orm import Session
import uuid
import textwrap

embedder = Embedder()

def chunk_and_store(video_id: str, transcript: str, db: Session):
    chunks = textwrap.wrap(transcript, 500)  # ~500 chars per chunk
    embeddings = embedder.encode(chunks)

    for text, emb in zip(chunks, embeddings):
        db_chunk = Chunk(
            id=str(uuid.uuid4()),
            video_id=video_id,
            text=text,
            embedding=emb
        )
        db.add(db_chunk)
    db.commit()
