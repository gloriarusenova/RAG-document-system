"""Reflex configuration file."""
import reflex as rx
from pathlib import Path

config = rx.Config(
    app_name="rag_chat_app",
    db_url="sqlite:///rag_chat.db",
    api_url="http://localhost:8000",
    env_file=str(Path(__file__).parent / ".env"),  # Load .env file
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],  # Disable sitemap plugin
)

