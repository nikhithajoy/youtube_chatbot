from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore
from app.llm.gemini_client import GeminiClient

class RAGPipeline:
    def __init__(self, db_url):
        self.embedder = Embedder()
        self.vectorstore = VectorStore(db_url)
        self.llm = GeminiClient()

    def query(self, user_query: str, top_k=3):
        vector = self.embedder.embed_text(user_query)
        results = self.vectorstore.semantic_search(vector, top_k)

        context = "\n\n".join([f"Title: {title}\nSummary: {summary}" for _, title, _, summary in results])
        prompt = f"""
User Query: {user_query}

Relevant Video Summaries:
{context}

Based on the above, recommend videos with brief explanation and links.
"""

        response = self.llm.generate(prompt)
        return response
