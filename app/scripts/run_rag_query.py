from app.rag.rag_pipeline import RAGPipeline
import os

pipeline = RAGPipeline(db_url=os.getenv("DATABASE_URL"))

query = input("Enter your question: ")
response = pipeline.query(query)
print("\n--- Answer ---\n")
print(response)
