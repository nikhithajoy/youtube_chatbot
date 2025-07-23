import psycopg2
from typing import List

class VectorStore:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def update_video_embedding(self, video_id: int, vector: List[float]):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE videos SET embedding = %s WHERE id = %s",
                (vector, video_id)
            )
            self.conn.commit()

    def semantic_search(self, query_vector: List[float], top_k=3):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, url, summary
                FROM videos
                ORDER BY embedding <-> %s
                LIMIT %s;
            """, (query_vector, top_k))
            return cur.fetchall()
