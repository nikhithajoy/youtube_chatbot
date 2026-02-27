from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import get_settings


settings = get_settings()   


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting YouTube Channel Chatbot...")
    print(f"Environment: {settings.ENVIRONMENT}")

    # TODO: Initialize DB connection
    # TODO: Initialize vector store
    # TODO: Warm up embedding model

    yield

    print("Shutting down application...")
    # TODO: Close DB connections
    # TODO: Gracefully shutdown background workers
    
    
app = FastAPI(
    title=settings.APP_NAME,
    description="A chatbot that answers questions about YouTube channels using OpenAI's language models and embeddings.",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }
    
    
# root endpoint
@app.get("/", tags=["System"])
async def root():
    return {
        "message": "YouTube Channel Chatbot API is running"
    }