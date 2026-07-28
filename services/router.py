"""
Question routing service.

This module routes user questions
to the appropriate retrieval workflow.
"""

from langchain_chroma import Chroma

from services.rag import answer_from_pdf
from services.web_rag import answer_from_web


def route_question(
    vector_store: Chroma,
    question: str,
) -> str:
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
        The generated answer.
    """

    pdf_answer = answer_from_pdf(
        vector_store,
        question,
    )

    if pdf_answer is not None:
        return pdf_answer

    return answer_from_web(
        question,
    )