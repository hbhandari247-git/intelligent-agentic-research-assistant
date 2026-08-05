"""
Context fusion service.

This module combines ranked retrieval
candidates into structured LLM context
and preserves their citations.
"""

from models.citation import Citation
from models.ranked_candidate import RankedCandidate


def fuse_context(
    ranked_candidates: list[RankedCandidate],
) -> str:
    """
    Combine ranked retrieval candidates
    into structured context.

    Source information is preserved so
    evidence from different retrieval
    systems remains distinguishable.
    """

    context_blocks = []

    for ranked_candidate in ranked_candidates:
        candidate = ranked_candidate.candidate
        citation = candidate.citation

        source_label = candidate.source.value

        header_parts = [
            source_label,
            citation.title,
            citation.location,
        ]

        header = " | ".join(part for part in header_parts if part)

        context_blocks.append(f"[{header}]\n{candidate.content}")

    return "\n\n".join(context_blocks)


def build_citations(
    ranked_candidates: list[RankedCandidate],
) -> list[Citation]:
    """
    Build unique citations from ranked
    retrieval candidates.

    Citation order follows candidate
    relevance order.
    """

    citations = []
    seen = set()

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
