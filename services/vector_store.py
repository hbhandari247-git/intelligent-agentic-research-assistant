"""
Vector store service.

This module creates or loads the Chroma
vector database used for semantic retrieval.
"""

import os

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config.settings import CHROMA_DB_PATH
from services.embeddings import embeddings


def get_vector_store(
    chunks: list[Document] | None = None,
) -> Chroma:
    """
    Load an existing Chroma vector store.

    If the database does not exist,
    create a new one using the
    supplied document chunks.

    Args:
        chunks:
            Document chunks used to create
            the vector store if it does not
            already exist.

    Returns:
        An initialized Chroma vector store.

    Raises:
        ValueError:
            If the database does not exist
            and no document chunks are
            provided.
    """

    if os.path.exists(CHROMA_DB_PATH):

        print("📂 Loading existing vector database...")

        return Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings,
        )

    print("🆕 Creating new vector database...")

    if chunks is None:
        raise ValueError(
            "Document chunks are required "
            "when creating a new vector database."
        )

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
    )
