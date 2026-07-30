"""
Question routing service.

This module routes user questions
to the appropriate retrieval workflow.
"""

from langchain_chroma import Chroma

from models.response import Response
from services.rag import answer_from_pdf
from services.web_rag import answer_from_web


def route_question(
    vector_store: Chroma,
    question: str,
) -> Response:
    """
    Route a user's question to the
    appropriate retrieval workflow.

    Workflow:

        1. Try answering from the PDF.
        2. If no relevant context exists,
           fall back to web search.

    Args:
        vector_store:
            The initialized Chroma vector store.

        question:
            The user's question.

    Returns:
        A response generated from either the PDF
        or web search.
    """

    response = answer_from_pdf(
        vector_store,
        question,
    )

    if response.found:
        return response

    return answer_from_web(
        question,
    )
