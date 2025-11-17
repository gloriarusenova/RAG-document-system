"""Metrics display component for middle column."""
import reflex as rx


def metrics_display(result, is_loading: bool = False) -> rx.Component:
    """Display evaluation metrics and answers in chat-like UI."""

    return rx.box(
        rx.vstack(
            # User question (right-aligned)
            rx.box(
                rx.box(
                    rx.text(
                        result.question,
                        font_size="16px",
                        color="white",
                        line_height="1.6",
                    ),
                    padding="16px",
                    bg="#3c4043",
                    border_radius="18px",
                    max_width="80%",
                ),
                width="100%",
                display="flex",
                justify_content="flex-end",
            ),
            
            # Spacer between question and answer (32px)
            rx.box(height="32px"),

            # AI answer (left-aligned)
            rx.hstack(
                # Avatar/Icon - just the blue sparkle
                rx.box(
                    rx.icon("sparkles", size=24, color="#8ab4f8"),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    mr="16px",
                ),
                # Answer bubble - show loading or actual answer
                rx.cond(
                    is_loading,
                    # Loading spinner
                    rx.box(
                        rx.spinner(
                            size="3",
                            color="#8ab4f8",
                        ),
                        padding="16px",
                        bg="transparent",
                        max_width="80%",
                    ),
                    # Actual answer
                    rx.box(
                        rx.text(
                            result.generated_answer,
                            font_size="16px",
                            color="#e8eaed",
                            line_height="1.6",
                        ),
                        padding="16px",
                        bg="transparent",
                        max_width="80%",
                    ),
                ),
                spacing="0",
                align="center",
                width="100%",
            ),
            
            spacing="0",
            width="100%",
        ),
        width="1200px",
        max_width="100%",
        mx="auto",
    )
