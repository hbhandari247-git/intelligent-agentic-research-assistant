"""
Retrieval-Augmented Generation (RAG) workflow.

This module orchestrates document retrieval
and answer generation.
"""

from pathlib import Path

from langchain_chroma import Chroma

from models.citation import Citation
from models.response import Response
from models.source import Source
from services.evaluator import (
    evaluate_pdf_retrieval,
)
from services.generator import (
    build_context,
    generate_answer,
)
from services.retriever import (
    retrieve_documents,
)


def answer_from_pdf(
    vector_store: Chroma,
    question: str,
) -> Response:
    """
    Answer a user's question using
    the indexed PDF.
    """

    retrieved_documents = retrieve_documents(
        vector_store,
        question,
    )

    evaluation = evaluate_pdf_retrieval(
        retrieved_documents,
    )

    if not evaluation.passed:
        return Response.empty()

    chunks = []
    citations = []
    seen = set()

    for document, _ in retrieved_documents:
        chunks.append(
            document.page_content,
        )

        metadata = document.metadata

        key = (
            metadata["source"],
            metadata["page"],
        )

        if key in seen:
            continue

        seen.add(key)

        citations.append(
            Citation(
                title=Path(
                    metadata["source"],
                ).name,
                location=f"Page {metadata['page'] + 1}",
            )
        )

    context = build_context(
        chunks,
    )

    citations.sort(key=lambda citation: int(citation.location.removeprefix("Page ")))

    return Response(
        answer=generate_answer(
            context,
            question,
        ),
        source=Source.PDF,
        confidence=evaluation.confidence,
        citations=citations,
    )
