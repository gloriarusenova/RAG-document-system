"""Evaluation results display component."""
import reflex as rx
from rag_chat_app.eval_state import RetrievedChunk


def render_chunk(chunk: RetrievedChunk) -> rx.Component:
    """Render a single retrieved chunk."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    "#" + chunk.rank.to_string(),
                    color_scheme="blue",
                    size="1",
                ),
                rx.cond(
                    chunk.is_relevant,
                    rx.badge(
                        rx.hstack(
                            rx.icon("check", size=12),
                            rx.text("RELEVANT"),
                            spacing="1",
                        ),
                        color_scheme="green",
                        size="1",
                    ),
                    rx.badge(
                        "Not Relevant",
                        color_scheme="gray",
                        size="1",
                    ),
                ),
                rx.text(
                    chunk.source_id,
                    font_size="11px",
                    color="gray.500",
                    font_family="monospace",
                ),
                spacing="2",
                width="100%",
                mb="2",
            ),
            rx.text(
                chunk.content,
                font_size="12px",
                color="gray.700",
                line_height="1.5",
                no_of_lines=3,  # Truncate to 3 lines
            ),
            align="start",
            spacing="1",
        ),
        p="3",
        bg=rx.cond(chunk.is_relevant, "green.50", "white"),
        border="1px solid",
        border_color=rx.cond(chunk.is_relevant, "green.300", "gray.200"),
        border_radius="md",
        mb="2",
    )


def eval_results(result) -> rx.Component:
    """Display evaluation results with metrics."""
    
    return rx.vstack(
        # Header with correctness badge
        rx.hstack(
            rx.heading("Evaluation Results", size="6"),
            rx.badge(
                rx.cond(
                    result.is_correct,
                    rx.hstack(
                        rx.icon("check", size=16),
                        rx.text("CORRECT"),
                        spacing="1",
                    ),
                    rx.hstack(
                        rx.icon("x-circle", size=16),
                        rx.text("INCORRECT"),
                        spacing="1",
                    ),
                ),
                color_scheme=rx.cond(result.is_correct, "green", "red"),
                size="3",
                variant="solid",
            ),
            width="100%",
            justify="between",
            align="center",
            mb="4",
            pb="3",
            border_bottom="2px solid",
            border_color="gray.200",
        ),
        
        # Question
        rx.box(
            rx.text("Question:", font_weight="600", font_size="14px", color="gray.600", mb="1"),
            rx.text(result.question, font_size="15px", color="gray.800"),
            mb="4",
        ),
        
        # Generated Answer
        rx.box(
            rx.text("Generated Answer:", font_weight="600", font_size="14px", color="gray.600", mb="1"),
            rx.box(
                rx.text(result.generated_answer, font_size="15px", line_height="1.6"),
                p="4",
                bg="blue.50",
                border_left="4px solid",
                border_color="blue.500",
                border_radius="md",
            ),
            mb="4",
        ),
        
        # Expected Answer
        rx.box(
            rx.text("Expected Answer:", font_weight="600", font_size="14px", color="gray.600", mb="1"),
            rx.box(
                rx.text(result.expected_answer, font_size="15px", line_height="1.6"),
                p="4",
                bg="green.50",
                border_left="4px solid",
                border_color="green.500",
                border_radius="md",
            ),
            mb="4",
        ),
        
        # AI Reasoning
        rx.box(
            rx.text("AI Evaluation Reasoning:", font_weight="600", font_size="14px", color="gray.600", mb="1"),
            rx.box(
                rx.text(result.reasoning, font_size="14px", line_height="1.6", color="gray.700"),
                p="4",
                bg="gray.50",
                border_radius="md",
            ),
            mb="4",
        ),
        
        # Metrics Section
        rx.box(
            rx.heading("Retrieval Metrics", size="5", mb="3"),
            
            rx.grid(
                # Precision
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("target", size=20, color="blue.600"),
                            rx.text("Precision", font_weight="600", font_size="16px"),
                            spacing="2",
                        ),
                        rx.text(
                            f"{(result.precision * 100):.1f}%",
                            font_size="32px",
                            font_weight="bold",
                            color="blue.600",
                        ),
                        rx.text(
                            "Retrieved chunks that are relevant",
                            font_size="12px",
                            color="gray.600",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    p="4",
                    bg="blue.50",
                    border_radius="lg",
                    border="1px solid",
                    border_color="blue.200",
                ),
                
                # Recall
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("check", size=20, color="green.600"),
                            rx.text("Recall", font_weight="600", font_size="16px"),
                            spacing="2",
                        ),
                        rx.text(
                            f"{(result.recall * 100):.1f}%",
                            font_size="32px",
                            font_weight="bold",
                            color="green.600",
                        ),
                        rx.text(
                            "Relevant chunks that were retrieved",
                            font_size="12px",
                            color="gray.600",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    p="4",
                    bg="green.50",
                    border_radius="lg",
                    border="1px solid",
                    border_color="green.200",
                ),
                
                # MRR
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("zap", size=20, color="orange.600"),
                            rx.text("MRR", font_weight="600", font_size="16px"),
                            spacing="2",
                        ),
                        rx.text(
                            f"{(result.mrr * 100):.1f}%",
                            font_size="32px",
                            font_weight="bold",
                            color="orange.600",
                        ),
                        rx.text(
                            "Mean Reciprocal Rank",
                            font_size="12px",
                            color="gray.600",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    p="4",
                    bg="orange.50",
                    border_radius="lg",
                    border="1px solid",
                    border_color="orange.200",
                ),
                
                columns="3",
                spacing="4",
                width="100%",
            ),
            
            # Retrieval stats
            rx.hstack(
                rx.badge(
                    f"Retrieved: {result.retrieved_count} chunks",
                    color_scheme="blue",
                    size="2",
                ),
                rx.badge(
                    f"Relevant: {result.relevant_count} chunks",
                    color_scheme="green",
                    size="2",
                ),
                spacing="2",
                mt="3",
            ),
            
            p="4",
            bg="white",
            border="1px solid",
            border_color="gray.200",
            border_radius="lg",
            mb="4",
        ),
        
        # Retrieved Chunks Section
        rx.box(
            rx.heading("Retrieved Chunks (Top 30)", size="5", mb="3"),
            rx.text(
                "Green background = relevant chunk, Gray = not relevant. Scroll to see all retrieved chunks.",
                font_size="13px",
                color="gray.600",
                mb="3",
            ),
            rx.vstack(
                rx.foreach(
                    result.retrieved_chunks,
                    render_chunk,
                ),
                width="100%",
                spacing="0",
                max_height="600px",
                overflow_y="auto",
            ),
            p="4",
            bg="white",
            border="1px solid",
            border_color="gray.200",
            border_radius="lg",
            mb="4",
        ),
        
        # Metrics explanation
        rx.box(
            rx.heading("Metrics Explained", size="4", mb="2"),
            rx.vstack(
                rx.text(
                    "• ",
                    rx.text("Precision:", font_weight="600", as_="span"),
                    " Of all chunks retrieved, what percentage were actually relevant?",
                    font_size="13px",
                    color="gray.700",
                ),
                rx.text(
                    "• ",
                    rx.text("Recall:", font_weight="600", as_="span"),
                    " Of all relevant chunks, what percentage were successfully retrieved?",
                    font_size="13px",
                    color="gray.700",
                ),
                rx.text(
                    "• ",
                    rx.text("MRR:", font_weight="600", as_="span"),
                    " How quickly did we find the first relevant chunk? (1/rank of first relevant chunk)",
                    font_size="13px",
                    color="gray.700",
                ),
                align="start",
                spacing="2",
            ),
            p="4",
            bg="gray.50",
            border_radius="md",
        ),
        
        width="100%",
        spacing="0",
    )

