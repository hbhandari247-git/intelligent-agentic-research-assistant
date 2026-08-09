"""
Context fusion service.

This module combines ranked retrieval
candidates into structured LLM context
while preserving citation information.
"""

from models.citation import Citation
from models.ranked_candidate import RankedCandidate


def fuse_context(
    ranked_candidates: list[RankedCandidate],
) -> str:
    """
    Combine ranked candidates into a
    structured context string.
    """

    context_blocks: list[str] = []

    for ranked_candidate in ranked_candidates:
        candidate = ranked_candidate.candidate
        citation = candidate.citation

        header = " | ".join(
            part
            for part in (
                candidate.source.value,
                citation.title,
                citation.location,
            )
            if part
        )

        context_blocks.append(f"[{header}]\n" f"{candidate.content}")

    return "\n\n".join(context_blocks)


def build_citations(
    ranked_candidates: list[RankedCandidate],
) -> list[Citation]:
    """
    Build unique citations in relevance order.
    """

    citations: list[Citation] = []

    seen: set[tuple[str, str, str | None]] = set()

    for ranked_candidate in ranked_candidates:
        citation = ranked_candidate.candidate.citation

        key = (
            citation.title,
            citation.location,
            citation.url,
        )

        if key in seen:
            continue

        seen.add(key)
        citations.append(citation)

    return citations
