"""
Application configuration.

This module contains all configurable
constants used throughout the application.
"""

from pathlib import Path

# -----------------------------
# Documents
# -----------------------------

DATA_DIR: Path = Path("data")

SUPPORTED_DOCUMENT_TYPES: tuple[str, ...] = (".pdf",)

# -----------------------------
# Vector Database
# -----------------------------

CHROMA_DB_PATH: Path = Path("db")

# -----------------------------
# Retrieval
# -----------------------------

TOP_K = 3

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100

# -----------------------------
# Embeddings
# -----------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -----------------------------
# LLM
# -----------------------------

MODEL_NAME = "openai/gpt-oss-20b"

TEMPERATURE = 0

# -----------------------------
# Web Search
# -----------------------------

TAVILY_MAX_RESULTS = 3

# -----------------------------
# Retrieval Evaluation
# -----------------------------

PDF_RETRIEVAL_THRESHOLD = 1.00

WEB_RETRIEVAL_THRESHOLD = 0.50

# -----------------------------
# Hybrid Retrieval
# -----------------------------

HYBRID_TOP_K = 5

# -----------------------------
# Conversation Memory
# -----------------------------

MAX_CONVERSATION_MESSAGES = 10

# -----------------------------
# Index Management
# -----------------------------

INDEX_MANIFEST_FILENAME = "manifest.json"
