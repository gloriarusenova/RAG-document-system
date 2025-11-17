"""Database models for chat persistence."""
import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime


class ChatMessage(rx.Model, table=True):
    """Store chat messages with persistence."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(index=True)
    question: str
    answer: str
    sources: Optional[str] = None  # JSON string of sources
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field(default="default_user")
    
    # Retrieval metrics
    avg_score: Optional[float] = None
    num_sources: Optional[int] = None
    top_score: Optional[float] = None
    score_variance: Optional[float] = None


class ChatSession(rx.Model, table=True):
    """Track chat sessions."""
    
    session_id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field(default="default_user")

