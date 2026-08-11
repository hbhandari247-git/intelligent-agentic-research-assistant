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

# Number of candidates ultimately expected
# to survive retrieval/reranking.
TOP_K = 12

# Retrieve a broader candidate pool before
# downstream reranking.
#
# Example:
#   TOP_K = 12
#   multiplier = 3
#   retrieval candidates = 36
#
# This is intentionally domain-agnostic.
RETRIEVAL_CANDIDATE_MULTIPLIER = 3

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100

# Maximum number of retrieved candidates exposed
# to the follow-up planner.
FOLLOW_UP_OBSERVATION_TOP_K = 6

# Maximum characters retained from each candidate
# when building follow-up planner observations.
FOLLOW_UP_OBSERVATION_MAX_CHARS = 1500

# Maximum number of candidates exposed to the
# final answer generator.
GENERATION_CONTEXT_TOP_K = 8

# Maximum characters retained from an individual
# candidate in the final generation context.
GENERATION_CONTEXT_MAX_CHARS = 4000

# -----------------------------
# Embeddings
# -----------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# -----------------------------
# LLM
# -----------------------------

# Fast, higher-quota model used during
# v3 stabilization.
MODEL_NAME = "llama-3.1-8b-instant"

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
