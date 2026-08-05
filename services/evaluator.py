"""
Retrieval evaluation service.

This module evaluates retrieval quality
before answer generation.
"""

from config.settings import (
    PDF_RETRIEVAL_THRESHOLD,
    WEB_RETRIEVAL_THRESHOLD,
)
from models.confidence import Confidence
from models.retrieval_evaluation import (
    RetrievalEvaluation,
)
from models.web_result import WebResult


def evaluate_pdf_retrieval(
    retrieved_documents: list[tuple],
    threshold: float = PDF_RETRIEVAL_THRESHOLD,
) -> RetrievalEvaluation:
    """
    Evaluate the quality of retrieved
    PDF documents.

    Args:
        retrieved_documents:
            Retrieved (Document, distance) pairs.

        threshold:
            Maximum acceptable retrieval distance.

    Returns:
        Retrieval evaluation result.
    """

    if not retrieved_documents:
        return RetrievalEvaluation(
            passed=False,
            confidence=Confidence.NONE,
            score=float("inf"),
        )

    best_distance = min(distance for _, distance in retrieved_documents)

    if best_distance <= 0.60:
        confidence = Confidence.VERY_HIGH

    elif best_distance <= 0.80:
        confidence = Confidence.HIGH

    elif best_distance <= threshold:
        confidence = Confidence.MEDIUM

    else:
        confidence = Confidence.LOW

    return RetrievalEvaluation(
        passed=best_distance <= threshold,
        confidence=confidence,
        score=best_distance,
    )


def evaluate_web_retrieval(
    results: list[WebResult],
    threshold: float = WEB_RETRIEVAL_THRESHOLD,
) -> RetrievalEvaluation:
    """
    Evaluate the quality of retrieved
    web search results.

    Args:
        results:
            Retrieved web search results.

        threshold:
            Minimum acceptable relevance score.

    Returns:
        Retrieval evaluation result.
    """

    if not results:
        return RetrievalEvaluation(
            passed=False,
            confidence=Confidence.NONE,
            score=0.0,
        )

    best_score = max(result.score for result in results)

    if best_score >= 0.90:
        confidence = Confidence.VERY_HIGH

    elif best_score >= 0.75:
        confidence = Confidence.HIGH

    elif best_score >= threshold:
        confidence = Confidence.MEDIUM

    else:
        confidence = Confidence.LOW

    return RetrievalEvaluation(
        passed=best_score >= threshold,
        confidence=confidence,
        score=best_score,
    )


def combine_confidence(
    pdf_confidence: Confidence,
    web_confidence: Confidence,
) -> Confidence:
    """
    Combine PDF and web retrieval confidence
    into a final hybrid confidence level.

    The stronger available retrieval confidence
    is used for the combined result.

    Args:
        pdf_confidence:
            Confidence from PDF retrieval.

        web_confidence:
            Confidence from web retrieval.

    Returns:
        Combined hybrid confidence.
    """

    confidence_rank = {
        Confidence.NONE: 0,
        Confidence.LOW: 1,
        Confidence.MEDIUM: 2,
        Confidence.HIGH: 3,
        Confidence.VERY_HIGH: 4,
    }

    return max(
        (
            pdf_confidence,
            web_confidence,
        ),
        key=confidence_rank.get,
    )
