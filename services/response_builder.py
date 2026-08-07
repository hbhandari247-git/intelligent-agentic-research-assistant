"""
Response builder service.

This module builds structured
responses from retrieval candidates.
"""

from config.settings import HYBRID_TOP_K
from models.confidence import Confidence
from models.ranked_candidate import RankedCandidate
from models.response import Response
from models.retrieval_candidate import RetrievalCandidate
from models.source import Source
from services.context_fusion import (
    build_citations,
    fuse_context,
)
from services.generator import generate_answer
from services.reranker import (
    rerank_candidates,
)


def _rank_candidates(
    question: str,
    candidates: list[RetrievalCandidate],
) -> list[RankedCandidate]:
    """
    Rerank candidates and retain only
    the strongest evidence.
    """

    return rerank_candidates(
        question,
        candidates,
    )[:HYBRID_TOP_K]


def build_response(
    question: str,
    candidates: list[RetrievalCandidate],
    source: Source,
    confidence: Confidence,
) -> Response:
    """
    Build a structured response
    from retrieval candidates.
    """

    ranked_candidates = _rank_candidates(
        question,
        candidates,
    )

    if not ranked_candidates:
        return Response.empty()

    context = fuse_context(
        ranked_candidates,
    )

    return Response(
        answer=generate_answer(
            context,
            question,
        ),
        source=source,
        confidence=confidence,
        citations=build_citations(
            ranked_candidates,
        ),
    )
