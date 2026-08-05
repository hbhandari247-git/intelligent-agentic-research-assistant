"""
Application configuration.

This module contains all configurable
constants used throughout the application.
"""

# -----------------------------
# Documents
# -----------------------------

PDF_PATH = "data/Attention_is_All_You_Need.pdf"

# -----------------------------
# Vector Database
# -----------------------------

CHROMA_DB_PATH = "db"

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

"""
Application configuration.
"""


# Retrieval settings
PDF_RETRIEVAL_THRESHOLD = 1.00
WEB_RETRIEVAL_THRESHOLD = 0.50

HYBRID_TOP_K = 5
