"""
Retrieval strategy service.

This module determines which retrieval
strategy should be used for a question.
"""

from models.confidence import Confidence
from models.retrieval_evaluation import RetrievalEvaluation
from models.retrieval_strategy import RetrievalStrategy


def determine_retrieval_strategy(
    pdf_evaluation: RetrievalEvaluation,
) -> RetrievalStrategy:
    """
    Determine the retrieval strategy from
    the PDF retrieval evaluation.

    Strong PDF retrieval uses the local
    knowledge base directly.

    Uncertain PDF retrieval supplements
    local context with web retrieval.

    Failed PDF retrieval uses web retrieval.
    """

    if not pdf_evaluation.passed:
        return RetrievalStrategy.WEB_ONLY

    if pdf_evaluation.confidence in {
        Confidence.VERY_HIGH,
        Confidence.HIGH,
    }:
        return RetrievalStrategy.PDF_ONLY

    return RetrievalStrategy.HYBRID
