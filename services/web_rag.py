"""
Web Retrieval-Augmented Generation (Web RAG) workflow.

This module orchestrates web retrieval
and answer generation.
"""

from services.generator import (
    build_context,
    generate_answer,
)

from services.web_search import (
    retrieve_from_web,
)


def answer_from_web(
    question: str,
) -> str | None:
    """
    Answer a user's question using
    web search results.

    Args:
        question:
            The user's question.

    Returns:
        The generated answer if
        relevant web results exist.

        Returns None otherwise.
    """

    chunks = retrieve_from_web(
        question,
    )

    if not chunks:
        return None

    context = build_context(
        chunks,
    )

    return generate_answer(
        context,
        question,
    )