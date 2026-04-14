"""
MiroOrca Backend Configuration
Loads and validates environment variables from .env
"""

import os
from dotenv import load_dotenv

# Load .env from project root (two levels up from this file)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))


class Config:
    # ── Flask ──────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    JSON_AS_ASCII = False  # Support non-ASCII characters in responses

    # ── File Upload ────────────────────────────────────────────────
    MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", 50))
    MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
    ALLOWED_EXTENSIONS = {"pdf", "md", "txt", "markdown"}

    # ── LLM — Default model (high-volume simulation rounds) ────────
    LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
    LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "gpt-4o-mini")

    # ── LLM — Smart model (report generation, ontology extraction) ─
    SMART_MODEL_NAME = os.environ.get("SMART_MODEL_NAME", None)
    SMART_API_KEY = os.environ.get("SMART_API_KEY", None)
    SMART_BASE_URL = os.environ.get("SMART_BASE_URL", None)

    # ── Neo4j ──────────────────────────────────────────────────────
    NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "miroorca")

    # ── Embeddings ─────────────────────────────────────────────────
    EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIMENSIONS = int(os.environ.get("EMBEDDING_DIMENSIONS", 768))
    EMBEDDING_BASE_URL = os.environ.get("EMBEDDING_BASE_URL", None)
    EMBEDDING_API_KEY = os.environ.get("EMBEDDING_API_KEY", None)

    # ── Simulation Defaults ────────────────────────────────────────
    DEFAULT_AGENT_COUNT = int(os.environ.get("DEFAULT_AGENT_COUNT", 100))

    # ── Simulation Platform Actions ────────────────────────────────
    TWITTER_ACTIONS = [
        "CREATE_POST",
        "REPOST",
        "LIKE_POST",
        "REPLY_TO_POST",
        "FOLLOW_USER",
        "SEARCH_POSTS",
    ]
    REDDIT_ACTIONS = [
        "CREATE_POST",
        "UPVOTE",
        "DOWNVOTE",
        "COMMENT",
        "REPLY_TO_COMMENT",
        "SEARCH_POSTS",
        "TREND",
    ]

    # ── Text Processing ────────────────────────────────────────────
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_CHUNK_OVERLAP = 50

    # ── Paths ──────────────────────────────────────────────────────
    SIMULATION_DATA_DIR = os.path.join(os.path.dirname(__file__), "../simulation_data")
    LOGS_DIR = os.path.join(os.path.dirname(__file__), "../logs")

    def validate(self):
        """Raise ValueError if required config is missing."""
        if not self.LLM_API_KEY:
            raise ValueError(
                "LLM_API_KEY is not set. "
                "Copy .env.example to .env and add your API key."
            )
        if not self.NEO4J_PASSWORD:
            raise ValueError("NEO4J_PASSWORD is not set.")
        return True


config = Config()
