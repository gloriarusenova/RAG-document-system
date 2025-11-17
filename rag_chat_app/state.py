"""State management for the RAG chat app."""
import reflex as rx
from typing import List, Optional
from datetime import datetime
import json
import uuid
from sqlmodel import select

from .models import ChatMessage, ChatSession
from .rag_service import get_rag_service


class SourceWithScore(rx.Base):
    """A source chunk with its similarity score."""
    content: str
    score: float


class Message(rx.Base):
    """In-memory message representation."""
    question: str
    answer: str
    sources: List[str] = []
    timestamp: str
    avg_score: float = 0.0
    quality_score: float = 0.0
    grade: str = "N/A"
    top_score: float = 0.0
    num_sources: int = 0
    score_variance: float = 0.0
    sources_with_scores: List[SourceWithScore] = []


class ChatState(rx.State):
    """State for the chat interface."""
    
    # Current session
    session_id: str = ""
    
    # Chat messages (in-memory for reactive UI)
    messages: List[Message] = []
    
    # Input
    current_question: str = ""
    
    # Loading state
    is_loading: bool = False
    
    # Error handling
    error_message: str = ""
    
    # Document count (for UI display)
    doc_count: int = 0
    
    # Modal state for score details
    show_score_modal: bool = False
    selected_message_idx: int = -1
    
    @rx.var
    def selected_message(self) -> Optional[Message]:
        """Get the currently selected message for modal display."""
        if 0 <= self.selected_message_idx < len(self.messages):
            return self.messages[self.selected_message_idx]
        return None
    
    def on_load(self):
        """Initialize session and load history."""
        # Create or get session ID
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
            self._create_session()
        
        # Load chat history from database
        self._load_chat_history()
        
        # Get document count
        try:
            rag_service = get_rag_service()
            self.doc_count = rag_service.get_document_count()
        except Exception as e:
            print(f"Error loading document count: {e}")
            self.doc_count = 0
    
    def set_question(self, value: str):
        """Update the current question input."""
        self.current_question = value
    
    def send_message(self):
        """Process user question and get AI response."""
        if not self.current_question.strip():
            return
        
        self.is_loading = True
        self.error_message = ""
        question = self.current_question
        self.current_question = ""  # Clear input immediately
        
        try:
            # Query RAG pipeline with scores
            rag_service = get_rag_service()
            result = rag_service.query_with_scores(question)
            
            retrieval_score = result["retrieval_score"]
            
            # Create message with scores
            message = Message(
                question=question,
                answer=result["answer"],
                sources=retrieval_score.sources[:3],  # Top 3 for display
                timestamp=datetime.now().strftime("%H:%M"),
                avg_score=retrieval_score.avg_score,
                quality_score=retrieval_score.quality_score,
                grade=retrieval_score.grade,
                top_score=retrieval_score.top_score,
                num_sources=retrieval_score.num_sources,
                score_variance=retrieval_score.score_variance,
                sources_with_scores=[
                    SourceWithScore(content=content, score=score)
                    for content, score in retrieval_score.sources_with_scores[:5]  # Top 5 for modal
                ]
            )
            
            # Add to UI (in-memory)
            self.messages.append(message)
            
            # Save to database
            self._save_message_to_db(message)
            
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"Error in send_message: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.is_loading = False
    
    def clear_chat(self):
        """Clear current chat session."""
        self.messages = []
        # Create new session
        self.session_id = str(uuid.uuid4())
        self._create_session()
    
    def open_score_modal(self, idx: int):
        """Open the score details modal for a specific message."""
        self.selected_message_idx = idx
        self.show_score_modal = True
    
    def close_score_modal(self):
        """Close the score details modal."""
        self.show_score_modal = False
        self.selected_message_idx = -1
    
    # Database operations
    
    def _create_session(self):
        """Create new chat session in database."""
        with rx.session() as session:
            chat_session = ChatSession(
                session_id=self.session_id,
                created_at=datetime.utcnow(),
                last_activity=datetime.utcnow()
            )
            session.add(chat_session)
            session.commit()
    
    def _load_chat_history(self):
        """Load chat history from database."""
        with rx.session() as session:
            statement = select(ChatMessage).where(
                ChatMessage.session_id == self.session_id
            ).order_by(ChatMessage.timestamp)
            db_messages = session.exec(statement).all()
            
            self.messages = [
                Message(
                    question=msg.question,
                    answer=msg.answer,
                    sources=json.loads(msg.sources) if msg.sources else [],
                    timestamp=msg.timestamp.strftime("%H:%M"),
                    avg_score=msg.avg_score or 0.0,
                    quality_score=msg.avg_score or 0.0,  # Use avg as quality for loaded messages
                    grade="N/A",
                    top_score=msg.top_score or 0.0,
                    num_sources=msg.num_sources or 0,
                    score_variance=msg.score_variance or 0.0,
                )
                for msg in db_messages
            ]
    
    def _save_message_to_db(self, message: Message):
        """Save message to database."""
        with rx.session() as session:
            chat_message = ChatMessage(
                session_id=self.session_id,
                question=message.question,
                answer=message.answer,
                sources=json.dumps(message.sources),
                timestamp=datetime.utcnow(),
                avg_score=message.avg_score,
                num_sources=message.num_sources,
                top_score=message.top_score,
                score_variance=message.score_variance,
            )
            session.add(chat_message)
            session.commit()
            
            # Update session activity
            statement = select(ChatSession).where(
                ChatSession.session_id == self.session_id
            )
            chat_session = session.exec(statement).first()
            if chat_session:
                chat_session.last_activity = datetime.utcnow()
                session.add(chat_session)
                session.commit()

