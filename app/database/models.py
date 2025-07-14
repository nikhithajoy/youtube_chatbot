from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class YouTubeChannel(Base):
    __tablename__ = "youtube_channels"

    id = Column(String, primary_key=True, index=True)  # channel_id
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String, nullable=False)

    videos = relationship("YouTubeVideo", back_populates="channel")


class YouTubeVideo(Base):
    __tablename__ = "youtube_videos"

    id = Column(String, primary_key=True, index=True)  # video_id
    channel_id = Column(String, ForeignKey("youtube_channels.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_sec = Column(Integer)
    transcription = Column(Text)
    url = Column(String, nullable=False)

    channel = relationship("YouTubeChannel", back_populates="videos")
