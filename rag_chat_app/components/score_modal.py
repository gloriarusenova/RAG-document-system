"""Score details modal component."""
import reflex as rx
from ..state import ChatState, Message


def score_modal() -> rx.Component:
    """
    Modal dialog showing detailed retrieval metrics.
    
    Displays:
    - Overall quality score and grade
    - Individual metric breakdowns
    - Source-by-source similarity scores
    """
    return rx.dialog.root(
        rx.dialog.content(
            # Header
            rx.dialog.title(
                rx.hstack(
                    rx.icon("bar-chart-2", size=24),
                    rx.text("Retrieval Quality Metrics"),
                    spacing="2",
                    align="center",
                )
            ),
            
            rx.dialog.description(
                "Detailed breakdown of how well the system retrieved relevant information for your question.",
                size="2",
                mb="4",
            ),
            
            # Content - only show if message is selected
            rx.cond(
                ChatState.selected_message != None,
                rx.vstack(
                    # Overall Score Section
                    rx.box(
                        rx.vstack(
                            rx.heading("Overall Quality", size="4", mb="2"),
                            rx.hstack(
                                rx.box(
                                    rx.text(
                                        ChatState.selected_message.grade,
                                        font_size="48px",
                                        font_weight="bold",
                                        color="green.600",
                                    ),
                                    text_align="center",
                                ),
                                rx.vstack(
                                    rx.text(
                                        ChatState.selected_message.quality_score.to(str),
                                        font_size="32px",
                                        font_weight="bold",
                                    ),
                                    rx.text(
                                        "out of 100",
                                        font_size="12px",
                                        color="gray.600",
                                    ),
                                    spacing="0",
                                    align="start",
                                ),
                                spacing="4",
                                align="center",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        p="4",
                        bg="green.50",
                        border_radius="md",
                        mb="4",
                    ),
                    
                    # Metrics Breakdown
                    rx.box(
                        rx.heading("Metrics Breakdown", size="4", mb="3"),
                        
                        # Average Similarity
                        rx.hstack(
                            rx.icon("target", size=16, color="blue.600"),
                            rx.text("Average Similarity:", font_weight="600", font_size="14px"),
                            rx.spacer(),
                            rx.badge(
                                f"{(ChatState.selected_message.avg_score * 100).to(int)}%",
                                color_scheme="blue",
                                size="2"
                            ),
                            width="100%",
                            mb="2",
                        ),
                        
                        # Top Score
                        rx.hstack(
                            rx.icon("award", size=16, color="purple.600"),
                            rx.text("Best Match:", font_weight="600", font_size="14px"),
                            rx.spacer(),
                            rx.badge(
                                f"{(ChatState.selected_message.top_score * 100).to(int)}%",
                                color_scheme="purple",
                                size="2"
                            ),
                            width="100%",
                            mb="2",
                        ),
                        
                        # Number of Sources
                        rx.hstack(
                            rx.icon("file-text", size=16, color="orange.600"),
                            rx.text("Sources Found:", font_weight="600", font_size="14px"),
                            rx.spacer(),
                            rx.badge(
                                ChatState.selected_message.num_sources.to(str),
                                color_scheme="orange",
                                size="2"
                            ),
                            width="100%",
                            mb="2",
                        ),
                        
                        # Score Consistency
                        rx.hstack(
                            rx.icon("trending-up", size=16, color="teal.600"),
                            rx.text("Consistency:", font_weight="600", font_size="14px"),
                            rx.spacer(),
                            rx.badge(
                                rx.cond(
                                    ChatState.selected_message.score_variance < 0.01,
                                    "High",
                                    rx.cond(
                                        ChatState.selected_message.score_variance < 0.05,
                                        "Medium",
                                        "Low"
                                    )
                                ),
                                color_scheme="teal",
                                size="2"
                            ),
                            width="100%",
                            mb="2",
                        ),
                        
                        p="4",
                        bg="gray.50",
                        border_radius="md",
                        mb="4",
                    ),
                    
                    # Top Sources with Scores
                    rx.box(
                        rx.heading("Top Retrieved Sources", size="4", mb="3"),
                        rx.vstack(
                            rx.foreach(
                                ChatState.selected_message.sources_with_scores,
                                lambda item, idx: rx.box(
                                    rx.hstack(
                                        rx.text(
                                            f"#{idx + 1}",
                                            font_weight="bold",
                                            color="gray.500",
                                            min_width="30px",
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                item.content[:100] + "...",
                                                font_size="12px",
                                                color="gray.700",
                                            ),
                                            rx.progress(
                                                value=(item.score * 100).to(int),
                                                max=100,
                                                size="1",
                                                color_scheme="blue",
                                            ),
                                            spacing="1",
                                            align="start",
                                            flex="1",
                                        ),
                                        rx.text(
                                            f"{(item.score * 100).to(int)}%",
                                            font_weight="600",
                                            font_size="13px",
                                            color="blue.600",
                                        ),
                                        spacing="3",
                                        align="start",
                                        width="100%",
                                    ),
                                    p="3",
                                    bg="white",
                                    border="1px solid",
                                    border_color="gray.200",
                                    border_radius="md",
                                    mb="2",
                                ),
                            ),
                            width="100%",
                            spacing="0",
                        ),
                        p="4",
                        bg="gray.50",
                        border_radius="md",
                    ),
                    
                    # Explanation
                    rx.box(
                        rx.vstack(
                            rx.heading("What do these metrics mean?", size="3", mb="2"),
                            rx.text(
                                "• ",
                                rx.text("Quality Score:", font_weight="600", as_="span"),
                                " Overall retrieval quality (0-100) based on similarity, consistency, and source count.",
                                font_size="12px",
                                color="gray.700",
                                mb="1",
                            ),
                            rx.text(
                                "• ",
                                rx.text("Average Similarity:", font_weight="600", as_="span"),
                                " How closely the retrieved sources match your question on average.",
                                font_size="12px",
                                color="gray.700",
                                mb="1",
                            ),
                            rx.text(
                                "• ",
                                rx.text("Best Match:", font_weight="600", as_="span"),
                                " The similarity score of the most relevant source found.",
                                font_size="12px",
                                color="gray.700",
                                mb="1",
                            ),
                            rx.text(
                                "• ",
                                rx.text("Consistency:", font_weight="600", as_="span"),
                                " How similar the scores are (high consistency = all sources equally relevant).",
                                font_size="12px",
                                color="gray.700",
                            ),
                            align="start",
                            spacing="1",
                        ),
                        p="4",
                        bg="blue.50",
                        border_radius="md",
                        border="1px solid",
                        border_color="blue.200",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                rx.text("No message selected", color="gray.500"),
            ),
            
            # Close button
            rx.dialog.close(
                rx.button(
                    "Close",
                    size="3",
                    variant="soft",
                    on_click=ChatState.close_score_modal,
                ),
            ),
            
            max_width="600px",
            max_height="80vh",
            overflow_y="auto",
        ),
        
        open=ChatState.show_score_modal,
        on_open_change=ChatState.close_score_modal,
    )

