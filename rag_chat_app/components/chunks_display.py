"""Chunks display component for right column."""
import reflex as rx
from rag_chat_app.eval_state import RetrievedChunk, EvalState


def render_chunk(chunk: RetrievedChunk) -> rx.Component:
    """Render a single retrieved chunk with expandable content."""
    # Check if this chunk is expanded
    is_expanded = EvalState.expanded_chunks.get(chunk.rank, False)
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    f"#{chunk.rank}",
                    font_size="12px",
                    color="#94a3b8",
                    font_weight="700",
                    min_width="35px",
                ),
                rx.cond(
                    chunk.is_relevant,
                    rx.badge(
                        rx.hstack(
                            rx.icon("check", size=12),
                            rx.text("Relevant", font_weight="600", font_size="11px"),
                            spacing="1",
                        ),
                        size="1",
                        bg="#dcfce7",
                        color="#16a34a",
                    ),
                    rx.badge(
                        "Not Relevant",
                        size="1",
                        bg="#f1f5f9",
                        color="#64748b",
                        font_weight="500",
                    ),
                ),
                rx.spacer(),
                rx.text(
                    chunk.source_id,
                    font_size="10px",
                    color="#94a3b8",
                    font_family="monospace",
                ),
                spacing="3",
                width="100%",
                align="center",
                mb="3",
            ),
            # Content
            rx.box(
                rx.text(
                    chunk.content,
                    font_size="13px",
                    color="#334155",
                    line_height="1.6",
                    no_of_lines=rx.cond(is_expanded, None, 3),
                ),
            ),
            # Show more/less button
            rx.cond(
                chunk.content.length() > 200,
                rx.button(
                    rx.hstack(
                        rx.text(
                            rx.cond(is_expanded, "Show less", "Show more"),
                            font_size="12px",
                            font_weight="600",
                        ),
                        rx.icon(
                            rx.cond(is_expanded, "chevron-up", "chevron-down"),
                            size=14,
                        ),
                        spacing="2",
                    ),
                    on_click=lambda: EvalState.toggle_chunk_expansion(chunk.rank),
                    size="1",
                    variant="ghost",
                    color="#6366f1",
                    mt="2",
                ),
                rx.box(),
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        p="4",
        bg=rx.cond(chunk.is_relevant, "#f0fdf4", "white"),
        border="1px solid",
        border_color=rx.cond(chunk.is_relevant, "#86efac", "#e5e7eb"),
        border_radius="8px",
        mb="3",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        _hover={"border_color": rx.cond(chunk.is_relevant, "#4ade80", "#cbd5e1")},
    )


def chunks_display(result) -> rx.Component:
    """Display retrieved chunks in the right column."""

    return rx.vstack(
        # Header
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Retrieved Chunks",
                        font_size="14px",
                        font_weight="600",
                        color="#475569",
                    ),
                    rx.spacer(),
                    rx.badge(
                        f"{result.retrieved_count} total",
                        size="2",
                        bg="#e0e7ff",
                        color="#6366f1",
                        font_weight="600",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.hstack(
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            bg="#dcfce7",
                            border_radius="4px",
                            border="2px solid #86efac",
                        ),
                        rx.text(
                            "Relevant",
                            font_size="12px",
                            color="#64748b",
                            font_weight="500",
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            bg="white",
                            border_radius="4px",
                            border="2px solid #e5e7eb",
                        ),
                        rx.text(
                            "Not Relevant",
                            font_size="12px",
                            color="#64748b",
                            font_weight="500",
                        ),
                        spacing="2",
                    ),
                    spacing="4",
                ),
                spacing="3",
            ),
            p="5",
            bg="white",
            border_radius="12px",
            border="1px solid #e5e7eb",
            mb="4",
            box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        ),

        # Chunks list
        rx.box(
            rx.vstack(
                rx.foreach(
                    result.retrieved_chunks,
                    render_chunk,
                ),
                width="100%",
                spacing="0",
            ),
            width="100%",
            max_height="600px",
            overflow_y="auto",
        ),
        
        width="100%",
        height="100%",
        spacing="0",
    )
