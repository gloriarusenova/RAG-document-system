"""Chat input component."""
import reflex as rx


def chat_input(on_submit, value: str, on_change, is_loading: bool) -> rx.Component:
    """
    Chat input field with send button.
    
    Args:
        on_submit: Function to call when submitting
        value: Current input value
        on_change: Function to call on input change
        is_loading: Whether request is in progress
    """
    return rx.form(
        rx.hstack(
            rx.input(
                placeholder="Ask a question about your documents...",
                value=value,
                on_change=on_change,
                disabled=is_loading,
                size="3",
                width="100%",
                variant="soft",
                name="question_input",
            ),
            rx.button(
                rx.cond(
                    is_loading,
                    rx.spinner(size="3"),
                    rx.icon("send", size=20),
                ),
                type="submit",
                disabled=is_loading,
                size="3",
                color_scheme="blue",
            ),
            spacing="2",
            width="100%",
        ),
        on_submit=on_submit,
        width="100%",
    )

