"""
Document retrieval service.

This module retrieves the most relevant
document chunks from the vector database.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config.settings import TOP_K


def retrieve_documents(
    vector_store: Chroma,
    question: str,
) -> list[tuple[Document, float]]:
    """
    Retrieve the most relevant document chunks
    along with their retrieval distances.

    Args:
        vector_store:
            The initialized Chroma vector store.

        question:
            The user's question.

    Returns:
        A list of tuples containing:

        - Document
        - Retrieval distance

        Lower distances indicate
        better semantic matches.
    """

    return vector_store.similarity_search_with_score(
        question,
        k=TOP_K,
    )
