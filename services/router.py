"""
Question routing service.

This module routes user questions
through the hybrid retrieval workflow.
"""

from langchain_chroma import Chroma

from models.response import Response
from services.hybrid_workflow import execute_hybrid_workflow


def route_question(
    vector_store: Chroma,
    question: str,
) -> Response:
    """
    Route a user's question through the
    hybrid retrieval workflow.

    The hybrid workflow determines whether
    to use PDF retrieval, web retrieval,
    or both based on retrieval quality.

    Args:
        vector_store:
            The initialized Chroma vector store.

        question:
            The user's question.

    Returns:
        The final structured response.
    """

    return execute_hybrid_workflow(
        vector_store,
        question,
    )
