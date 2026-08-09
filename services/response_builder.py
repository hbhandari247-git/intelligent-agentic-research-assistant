"""
Response builder service.

This module builds structured responses
from agent tool results.
"""

from collections import defaultdict

from config.settings import HYBRID_TOP_K
from models.confidence import Confidence
from models.ranked_candidate import RankedCandidate
from models.response import Response
from models.retrieval_candidate import RetrievalCandidate
from models.source import Source
from models.tool_result import ToolResult
from services.context_fusion import (
    build_citations,
    fuse_context,
)
from services.evaluator import (
    combine_confidence,
    evaluate_pdf_retrieval,
    evaluate_web_retrieval,
)
from services.generator import generate_answer
from services.reranker import rerank_candidates


def _rank_candidates(
    question: str,
    candidates: list[RetrievalCandidate],
) -> list[RankedCandidate]:
    """
    Rerank retrieval candidates and retain
    the strongest evidence.

    When multiple retrieval sources contribute
    candidates, ensure that each contributing
    source receives representation in the
    final evidence set before filling the
    remaining slots by semantic relevance.

    This prevents a highly relevant source from
    completely crowding out another source that
    was explicitly selected by the planner.

    The reranker itself remains source-agnostic.
    """

    ranked_candidates = rerank_candidates(
        question,
        candidates,
    )

    if not ranked_candidates:
        return []

    if HYBRID_TOP_K <= 0:
        return []

    # --------------------------------------------------
    # Group candidates by their source.
    #
    # This is intentionally dynamic. No specific
    # source names are required here, so adding a new
    # retrieval source does not require changing the
    # selection logic.
    # --------------------------------------------------

    candidates_by_source: dict[
        Source,
        list[RankedCandidate],
    ] = defaultdict(list)

    for candidate in ranked_candidates:
        candidates_by_source[candidate.candidate.source].append(candidate)

    # --------------------------------------------------
    # If only one source contributed candidates,
    # normal top-k relevance ranking is sufficient.
    # --------------------------------------------------

    if len(candidates_by_source) <= 1:
        return ranked_candidates[:HYBRID_TOP_K]

    # --------------------------------------------------
    # Multiple sources contributed evidence.
    #
    # Reserve one slot for the strongest candidate
    # from each source.
    #
    # This guarantees that a source explicitly selected
    # by the planner cannot disappear merely because
    # another source has slightly higher embedding
    # similarity.
    # --------------------------------------------------

    selected: list[RankedCandidate] = []

    for source_candidates in candidates_by_source.values():
        selected.append(
            source_candidates[0],
        )

    # --------------------------------------------------
    # Fill remaining slots using global relevance.
    #
    # This preserves the normal semantic ranking
    # behavior after source representation is ensured.
    # --------------------------------------------------

    selected_ids = {id(candidate) for candidate in selected}

    for candidate in ranked_candidates:
        if len(selected) >= HYBRID_TOP_K:
            break

        if id(candidate) in selected_ids:
            continue

        selected.append(candidate)
        selected_ids.add(
            id(candidate),
        )

    # --------------------------------------------------
    # Keep the final context ordered by semantic
    # relevance rather than by source.
    # --------------------------------------------------

    return sorted(
        selected,
        key=lambda candidate: candidate.relevance_score,
        reverse=True,
    )


def _extract_candidates(
    tool_results: tuple[ToolResult, ...],
) -> list[RetrievalCandidate]:
    """
    Extract retrieval candidates from
    successful tool results that produced
    usable content.
    """

    candidates: list[RetrievalCandidate] = []

    for result in tool_results:
        if not result.has_relevant_content:
            continue

        if result.knowledge is None:
            continue

        candidates.extend(
            result.knowledge.candidates,
        )

    return candidates


def _determine_source(
    ranked_candidates: list[RankedCandidate],
) -> Source | None:
    """
    Determine the response source from
    candidates that actually survived
    cross-source reranking.

    This prevents weak or rejected retrieval
    results from affecting the reported source.
    """

    sources = {
        ranked_candidate.candidate.source for ranked_candidate in ranked_candidates
    }

    if sources == {Source.PDF}:
        return Source.PDF

    if sources == {Source.WEB}:
        return Source.WEB

    if Source.PDF in sources and Source.WEB in sources:
        return Source.HYBRID

    return None


def _confidence_rank(
    confidence: Confidence,
) -> int:
    """
    Return the relative strength of a
    confidence level.
    """

    ranks = {
        Confidence.NONE: 0,
        Confidence.LOW: 1,
        Confidence.MEDIUM: 2,
        Confidence.HIGH: 3,
        Confidence.VERY_HIGH: 4,
    }

    return ranks[confidence]


def _confidence_from_ranked_candidates(
    ranked_candidates: list[RankedCandidate],
) -> Confidence:
    """
    Estimate confidence from the evidence
    that actually survived reranking.

    Confidence is based on the semantic
    relevance scores produced by the common
    cross-source reranker.

    This avoids reporting high confidence
    based only on raw retrieval scores.
    """

    if not ranked_candidates:
        return Confidence.NONE

    scores = [candidate.relevance_score for candidate in ranked_candidates]

    best_score = max(scores)

    if best_score >= 0.85:
        return Confidence.VERY_HIGH

    if best_score >= 0.75:
        return Confidence.HIGH

    if best_score >= 0.65:
        return Confidence.MEDIUM

    return Confidence.LOW


def _evaluate_source_confidence(
    tool_results: tuple[ToolResult, ...],
    ranked_candidates: list[RankedCandidate],
) -> Confidence:
    """
    Evaluate retrieval confidence using
    only sources that contributed ranked
    evidence.

    Source-specific retrieval evaluation
    is used as supporting evidence, while
    the final result is constrained by the
    semantic relevance of the ranked candidates.
    """

    ranked_sources = {candidate.candidate.source for candidate in ranked_candidates}

    pdf_confidence: Confidence | None = None
    web_confidence: Confidence | None = None

    if Source.PDF in ranked_sources:
        for result in tool_results:
            if not result.has_relevant_content:
                continue

            if result.knowledge is None:
                continue

            if not hasattr(
                result.knowledge,
                "retrieved_documents",
            ):
                continue

            evaluation = evaluate_pdf_retrieval(
                result.knowledge.retrieved_documents,
            )

            if pdf_confidence is None or _confidence_rank(
                evaluation.confidence,
            ) > _confidence_rank(
                pdf_confidence,
            ):
                pdf_confidence = evaluation.confidence

    if Source.WEB in ranked_sources:
        for result in tool_results:
            if not result.has_relevant_content:
                continue

            if result.knowledge is None:
                continue

            if not hasattr(
                result.knowledge,
                "results",
            ):
                continue

            evaluation = evaluate_web_retrieval(
                result.knowledge.results,
            )

            if web_confidence is None or _confidence_rank(
                evaluation.confidence,
            ) > _confidence_rank(
                web_confidence,
            ):
                web_confidence = evaluation.confidence

    semantic_confidence = _confidence_from_ranked_candidates(
        ranked_candidates,
    )

    if pdf_confidence is not None and web_confidence is not None:
        source_confidence = combine_confidence(
            pdf_confidence,
            web_confidence,
        )

    elif pdf_confidence is not None:
        source_confidence = pdf_confidence

    elif web_confidence is not None:
        source_confidence = web_confidence

    else:
        source_confidence = Confidence.NONE

    return min(
        (
            source_confidence,
            semantic_confidence,
        ),
        key=_confidence_rank,
    )


def _evaluate_confidence(
    tool_results: tuple[ToolResult, ...],
    ranked_candidates: list[RankedCandidate],
) -> Confidence:
    """
    Evaluate final confidence using:

    1. Source-specific retrieval quality.
    2. Cross-source semantic relevance.

    The weaker signal determines the final
    confidence so that weak evidence cannot
    produce an artificially high-confidence answer.
    """

    return _evaluate_source_confidence(
        tool_results,
        ranked_candidates,
    )


def build_response(
    question: str,
    tool_results: tuple[ToolResult, ...],
) -> Response:
    """
    Build the final structured response
    directly from agent tool results.

    Only evidence that survives cross-source
    reranking is used for:

    - answer generation
    - source determination
    - confidence calculation
    - citations

    Args:
        question:
            Original user question.

        tool_results:
            Results produced by the agent's
            executed tools.

    Returns:
        Final structured response.
    """

    candidates = _extract_candidates(
        tool_results,
    )

    if not candidates:
        return Response.empty()

    ranked_candidates = _rank_candidates(
        question,
        candidates,
    )

    if not ranked_candidates:
        return Response.empty()

    context = fuse_context(
        ranked_candidates,
    )

    source = _determine_source(
        ranked_candidates,
    )

    if source is None:
        return Response.empty()

    confidence = _evaluate_confidence(
        tool_results,
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
