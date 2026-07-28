"""
Document retrieval service.

This module retrieves the most relevant
document chunks from the vector database.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config.settings import (
    MAX_SIMILARITY_SCORE,
    TOP_K,
)


def retrieve_documents(
    vector_store: Chroma,
    question: str,
) -> list[tuple[Document, float]]:
    """
    Retrieve the most relevant document chunks
    along with their similarity scores.

    Args:
        vector_store:
            The initialized Chroma vector store.

        question:
            The user's question.

    Returns:
        A list of tuples containing:

        - Document
        - Similarity score

        Lower similarity scores indicate
        better semantic matches.
    """

    return vector_store.similarity_search_with_score(
        question,
        k=TOP_K,
    )


def get_best_score(
    results: list[tuple[Document, float]],
) -> float:
    """
    Return the lowest similarity score
    from the retrieved documents.

    Args:
        results:
            Retrieved documents with scores.

    Returns:
        The best (lowest) similarity score.

        Returns positive infinity if
        no documents are retrieved.
    """

    if not results:
        return float("inf")

    _, score = results[0]

    return score


def has_relevant_context(
    results: list[tuple[Document, float]],
) -> bool:
    """
    Determine whether the retrieved
    documents contain enough relevant
    context to answer the user's question.

    Args:
        results:
            Retrieved documents with scores.

    Returns:
        True if the best similarity score
        is below the configured threshold.

        False otherwise.
    """

    return (
        get_best_score(results)
        < MAX_SIMILARITY_SCORE
    )