"""Main Reflex app - RAG Evaluation Interface."""
import reflex as rx
from .eval_state import EvalState
from .components.metrics_display import metrics_display


def index() -> rx.Component:
    """Main evaluation interface page."""
    return rx.fragment(
        # Custom CSS for dark dropdown and input
        rx.html(
            """
            <style>
                /* Input and textarea placeholder styling */
                input::placeholder,
                textarea::placeholder {
                    color: #9aa0a6 !important;
                    opacity: 1 !important;
                }
                input::-webkit-input-placeholder,
                textarea::-webkit-input-placeholder {
                    color: #9aa0a6 !important;
                    opacity: 1 !important;
                }
                input::-moz-placeholder,
                textarea::-moz-placeholder {
                    color: #9aa0a6 !important;
                    opacity: 1 !important;
                }
                input:-ms-input-placeholder,
                textarea:-ms-input-placeholder {
                    color: #9aa0a6 !important;
                    opacity: 1 !important;
                }
                
                /* Dropdown styling */
                .dark-select [role="combobox"],
                .dark-select button[data-radix-collection-item] {
                    background-color: #3c4043 !important;
                    color: #9aa0a6 !important;
                }
                .dark-select .rt-SelectRoot,
                .dark-select > div {
                    width: 200px !important;
                    max-width: 200px !important;
                }
                .dark-select .rt-SelectTrigger {
                    background-color: transparent !important;
                    color: #9aa0a6 !important;
                    border: none !important;
                    outline: none !important;
                    box-shadow: none !important;
                    padding-right: 4px !important;
                    padding-left: 0px !important;
                    display: flex !important;
                    justify-content: flex-start !important;
                    align-items: center !important;
                    width: 200px !important;
                    max-width: 200px !important;
                }
                .dark-select .rt-SelectTrigger:focus,
                .dark-select .rt-SelectTrigger:hover,
                .dark-select .rt-SelectTrigger[data-state="open"] {
                    border: none !important;
                    outline: none !important;
                    box-shadow: none !important;
                }
                .dark-select .rt-SelectTrigger > span:first-child {
                    color: #9aa0a6 !important;
                    flex: 1 1 auto !important;
                    white-space: nowrap !important;
                    overflow: hidden !important;
                    text-overflow: ellipsis !important;
                    max-width: 110px !important;
                }
                .dark-select .rt-SelectTrigger svg {
                    flex-shrink: 0 !important;
                    margin-left: 0px !important;
                }
                [data-radix-popper-content-wrapper] {
                    z-index: 9999 !important;
                }
                .rt-SelectContent {
                    background-color: #3c4043 !important;
                    border: 1px solid #5f6368 !important;
                }
                .rt-SelectItem {
                    background-color: #3c4043 !important;
                    color: #e8eaed !important;
                }
                .rt-SelectItem:hover,
                .rt-SelectItem[data-highlighted] {
                    background-color: #5f6368 !important;
                    color: #ffffff !important;
                }
            </style>
            """
        ),
        rx.box(
        # Main content with flex layout
        rx.box(
            # Spacer at top for 120px padding
            rx.box(height="120px"),
            
            # Top section - Heading and subtitle
            rx.center(
                rx.vstack(
                    # Title
                    rx.heading(
                        rx.text("Ask me anything about ", as_="span", color="#e8eaed"),
                        rx.text("AuraTech", as_="span", color="#8ab4f8"),
                        size="9",
                        font_weight="700",
                        letter_spacing="-0.03em",
                        text_align="center",
                    ),
                    # Subheading (example question)
                    rx.cond(
                        EvalState.suggested_questions.length() > 0,
                        rx.text(
                            EvalState.suggested_questions[0].question,
                            font_size="16px",
                            color="#9aa0a6",
                            line_height="1.6",
                            text_align="center",
                        ),
                        rx.text(
                            "Try asking a question",
                            font_size="16px",
                            color="#9aa0a6",
                            line_height="1.6",
                            text_align="center",
                        ),
                    ),
                    spacing="3",
                    align="center",
                    max_width="800px",
                    width="100%",
                ),
                width="100%",
                px="8",
            ),
            
            # Spacer between subtitle and results (70px)
            rx.box(height="70px"),
            
            # Error message
            rx.cond(
                EvalState.error_message != "",
                rx.center(
                    rx.box(
                        rx.callout(
                            EvalState.error_message,
                            icon="circle_alert",
                            color_scheme="red",
                            variant="soft",
                            size="2",
                        ),
                        max_width="1200px",
                        width="100%",
                        mb="6",
                    ),
                ),
                rx.box(),
            ),

            # Middle section - Results (if any)
            rx.box(
                rx.center(
                    rx.box(
                        rx.cond(
                            EvalState.current_result != None,
                            metrics_display(EvalState.current_result, EvalState.is_evaluating),
                            rx.box(),
                        ),
                        max_width="900px",
                        width="100%",
                    ),
                    width="100%",
                    px="8",
                ),
                flex="1",
                overflow_y="auto",
                mt="40px",
            ),
            
            # Bottom section - Input field with dropdown below
            rx.box(
                rx.center(
                    rx.box(
                        # Input field with submit button and dropdown inside
                        rx.box(
                            # Text input area at the top
                            rx.text_area(
                                placeholder="Ask me something about AuraTech",
                                value=EvalState.custom_question_input,
                                on_change=EvalState.set_custom_question,
                                size="3",
                                width="100%",
                                bg="transparent",
                                color="#9aa0a6",
                                border="none",
                                _focus={"outline": "none", "box_shadow": "none", "color": "#e8eaed"},
                                _placeholder={"color": "#9aa0a6"},
                                style={
                                    "padding_right": "50px",
                                    "padding_left": "12px",
                                    "padding_top": "8px",
                                    "padding_bottom": "4px",
                                    "min_height": "60px",
                                    "max_height": "120px",
                                    "border": "none",
                                    "outline": "none",
                                    "box_shadow": "none",
                                    "resize": "vertical",
                                },
                            ),
                            # Dropdown below the text input, inside the field
                            rx.box(
                                rx.select(
                                    EvalState.question_options,
                                    placeholder="Select a question",
                                    on_change=EvalState.handle_dropdown_select,
                                    size="1",
                                    width="200px",
                                    color="#9aa0a6",
                                    high_contrast=False,
                                ),
                                padding_left="12px",
                                padding_bottom="8px",
                                padding_top="0px",
                                width="auto",
                                class_name="dark-select",
                            ),
                            # Submit button on the right top
                            rx.button(
                                rx.icon("circle-arrow-right", size=24),
                                on_click=EvalState.submit_custom_question,
                                disabled=EvalState.is_evaluating | (EvalState.custom_question_input == ""),
                                size="3",
                                variant="ghost",
                                position="absolute",
                                right="5px",
                                top="8px",
                                color="#8ab4f8",
                                _hover={"bg": "transparent", "color": "#aecbfa"},
                                _disabled={"color": "#5f6368", "cursor": "not-allowed"},
                                z_index="10",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            position="relative",
                            width="100%",
                            bg="transparent",
                            border="1px solid #5f6368",
                            border_radius="8px",
                            _focus_within={"border_color": "#8ab4f8"},
                            overflow="hidden",
                        ),
                        width="600px",
                        max_width="90%",
                    ),
                    width="100%",
                    px="8",
                ),
                width="100%",
                pt="4",
                bg="#202124",
            ),
            
            # Spacer at bottom for 120px padding
            rx.box(height="120px"),

            display="flex",
            flex_direction="column",
            bg="#202124",
            min_height="100vh",
        ),

        on_mount=EvalState.on_load,
        min_height="100vh",
        bg="#202124",
        ),
    )


# Create app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
    )
)

# Add page
app.add_page(
    index, 
    route="/", 
    title="RAG Evaluation Dashboard",
    description="Evaluate RAG system performance with test questions"
)
