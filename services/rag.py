"""
Retrieval-Augmented Generation (RAG) workflow.

This module orchestrates document retrieval
and answer generation.
"""

from langchain_chroma import Chroma

from services.generator import (
    build_context,
    generate_answer,
)

from services.retriever import (
    has_relevant_context,
    retrieve_documents,
)


def answer_from_pdf(
    vector_store: Chroma,
    question: str,
) -> str | None:
    """
    Answer a user's question using
    the indexed PDF.

    Workflow:

        1. Retrieve relevant documents.
        2. Check context relevance.
        3. Build context.
        4. Generate the answer.

    Args:
        vector_store:
            The initialized Chroma vector store.

        question:
            The user's question.

    Returns:
        The generated answer if the
        PDF contains relevant information.

        Returns None otherwise.
    """

    retrieved_documents = retrieve_documents(
        vector_store,
        question,
    )

    if not has_relevant_context(
        retrieved_documents,
    ):
        return None

    chunks = [
        document.page_content
        for document, _ in retrieved_documents
    ]

    context = build_context(
        chunks,
    )

    return generate_answer(
        context,
        question,
    )
