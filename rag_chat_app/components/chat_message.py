"""Individual chat message component."""
import reflex as rx
from typing import List


def chat_message(
    question: str, 
    answer: str, 
    sources: List[str], 
    timestamp: str,
    quality_score: float,
    grade: str,
    message_idx: int,
    on_score_click
) -> rx.Component:
    """
    Display a single Q&A pair with clickable quality score.
    
    Args:
        question: User's question
        answer: AI-generated answer
        sources: List of source chunks
        timestamp: Time of message
        quality_score: Overall quality score (0-100)
        grade: Letter grade (A+, A, B+, etc.)
        message_idx: Index in messages list (for click handler)
        on_score_click: Function to call when score is clicked
    """
    
    return rx.box(
        # Question
        rx.hstack(
            rx.icon("user", size=20, color="blue.600"),
            rx.text(
                question, 
                font_weight="600", 
                font_size="16px",
                color="gray.800"
            ),
            spacing="2",
            align="center",
            mb="3",
        ),
        
        # Answer
        rx.box(
            rx.text(
                answer, 
                font_size="15px", 
                line_height="1.7",
                color="gray.700"
            ),
            bg="gray.50",
            p="4",
            border_radius="md",
            mb="3",
        ),
        
        # Sources and Score row
        rx.hstack(
            # Sources section (always show, but conditional content)
            rx.cond(
                sources.length() > 0,
                rx.vstack(
                    rx.text(
                        "📄 Sources:", 
                        font_size="12px", 
                        font_weight="600", 
                        color="gray.600"
                    ),
                    rx.foreach(
                        sources[:2],  # Show top 2
                        lambda source: rx.text(
                            f"• {source[:80]}...",
                            font_size="11px",
                            color="gray.500",
                        ),
                    ),
                    align="start",
                    spacing="1",
                    flex="1",
                ),
                rx.box(),  # Empty box when no sources
            ),
            
            rx.spacer(),
            
            # Quality Score Badge (Clickable)
            # Color scheme determined by grade using rx.cond
            rx.tooltip(
                rx.badge(
                    rx.hstack(
                        rx.text(grade, font_weight="bold"),
                        rx.text(quality_score, font_size="11px"),
                        rx.icon("info", size=12),
                        spacing="1",
                        align="center",
                    ),
                    color_scheme=rx.cond(
                        grade.contains("A"),
                        "green",
                        rx.cond(
                            grade.contains("B"),
                            "blue",
                            "orange"
                        )
                    ),
                    size="2",
                    variant="solid",
                    cursor="pointer",
                    on_click=lambda: on_score_click(message_idx),
                    _hover={"opacity": 0.8, "transform": "scale(1.05)"},
                    transition="all 0.2s",
                ),
                content="Click to view detailed metrics"
            ),
            
            width="100%",
            align="start",
            mb="2",
        ),
        
        # Timestamp
        rx.text(
            timestamp, 
            font_size="10px", 
            color="gray.400", 
            text_align="right"
        ),
        
        p="4",
        border="1px solid",
        border_color="gray.200",
        border_radius="lg",
        mb="4",
        width="100%",
        bg="white",
        box_shadow="sm",
    )

