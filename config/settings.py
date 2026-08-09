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

TOP_K = 12

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100


# -----------------------------
# Embeddings
# -----------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# -----------------------------
# LLM
# -----------------------------

MODEL_NAME = "llama-3.3-70b-versatile"

TEMPERATURE = 0


# -----------------------------
# Web Search
# -----------------------------

TAVILY_MAX_RESULTS = 5


# -----------------------------
# Retrieval Evaluation
# -----------------------------

PDF_RETRIEVAL_THRESHOLD = 1.00

WEB_RETRIEVAL_THRESHOLD = 0.50


# -----------------------------
# Cross-source Reranking
# -----------------------------

HYBRID_TOP_K = 8


# -----------------------------
# Conversation Memory
# -----------------------------

MAX_CONVERSATION_MESSAGES = 10


# -----------------------------
# Index Management
# -----------------------------

INDEX_MANIFEST_FILENAME = "manifest.json"


# -----------------------------
# Agent Max Iterations / Executions
# -----------------------------

MAX_AGENT_ITERATIONS = 3

MAX_TOOL_EXECUTIONS_PER_RUN = 2
