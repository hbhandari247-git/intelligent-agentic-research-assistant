"""
Retrieval candidate builder service.

This module converts source-specific retrieval
results into normalized retrieval candidates.
"""

from langchain_core.documents import Document

from models.citation import Citation
from models.retrieval_candidate import RetrievalCandidate
from models.source import Source
from models.web_result import WebResult


def build_pdf_candidates(
    retrieved_documents: list[tuple[Document, float]],
) -> list[RetrievalCandidate]:
    """
    Convert retrieved documents into
    normalized retrieval candidates.
    """

    candidates: list[RetrievalCandidate] = []

    for document, score in retrieved_documents:

        metadata = document.metadata

        source_file = metadata.get(
            "source_file",
            metadata.get("source", "Document"),
        )

        page = metadata.get("page")

        location = f"Page {page + 1}" if isinstance(page, int) else "Document"

        candidates.append(
            RetrievalCandidate(
                content=document.page_content,
                source=Source.PDF,
                score=score,
                citation=Citation(
                    title=source_file,
                    location=location,
                ),
            )
        )

    return candidates


def build_web_candidates(
    results: list[WebResult],
) -> list[RetrievalCandidate]:
    """
    Convert web search results into
    normalized retrieval candidates.
    """

    return [
        RetrievalCandidate(
            content=result.content,
            source=Source.WEB,
            score=result.score,
            citation=Citation(
                title=result.title,
                location="Web",
                url=result.url,
            ),
        )
        for result in results
    ]
