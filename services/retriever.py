"""
Document retrieval service.

This module retrieves relevant document
chunks from the vector database.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config.settings import TOP_K


def retrieve_documents(
    vector_store: Chroma,
    question: str,
) -> list[tuple[Document, float]]:
    """
    Retrieve the most relevant document
    chunks together with their distances.
    """

    return vector_store.similarity_search_with_score(
        query=question,
        k=TOP_K,
    )
