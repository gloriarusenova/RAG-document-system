"""Question selector component with dropdown and suggestions."""
import reflex as rx
from ..eval_state import EvalState


def question_selector() -> rx.Component:
    """Question selector with dropdown."""

    return rx.vstack(
        # Dropdown for all questions
        rx.box(
            rx.vstack(
                rx.text(
                    "Select a Question",
                    font_size="14px",
                    font_weight="600",
                    color="#475569",
                    mb="3",
                ),
                rx.select(
                    EvalState.question_options,
                    placeholder="Choose a question...",
                    value=EvalState.selected_question,
                    on_change=EvalState.select_question,
                    size="3",
                    width="100%",
                ),
                spacing="0",
                width="100%",
            ),
            p="5",
            bg="white",
            border_radius="12px",
            border="1px solid #e5e7eb",
            mb="6",
            box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        ),
        
        # Selected question display
        rx.cond(
            EvalState.selected_question != "",
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("check-circle", size=18, color="#10b981"),
                        rx.text(
                            "Selected Question",
                            font_size="13px",
                            font_weight="600",
                            color="#10b981",
                        ),
                        spacing="2",
                    ),
                    rx.text(
                        EvalState.selected_question,
                        font_size="14px",
                        color="#1e293b",
                        line_height="1.6",
                        font_weight="500",
                    ),
                    align="start",
                    spacing="3",
                ),
                p="4",
                bg="#f0fdf4",
                border="1px solid #86efac",
                border_radius="8px",
                mb="6",
            ),
            rx.box(),
        ),

        # Evaluate button
        rx.button(
            rx.cond(
                EvalState.is_evaluating,
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text("Evaluating...", font_size="15px", font_weight="600"),
                    spacing="3",
                ),
                rx.hstack(
                    rx.icon("play", size=18),
                    rx.text("Get Answer", font_size="15px", font_weight="600"),
                    spacing="3",
                ),
            ),
            on_click=EvalState.evaluate_selected_question,
            disabled=EvalState.is_evaluating | (EvalState.selected_question == ""),
            size="3",
            width="100%",
            bg="#6366f1",
            color="white",
            border_radius="8px",
            _hover={"bg": "#4f46e5"},
            _disabled={"bg": "#cbd5e1", "cursor": "not-allowed"},
        ),

        width="100%",
        spacing="0",
    )

