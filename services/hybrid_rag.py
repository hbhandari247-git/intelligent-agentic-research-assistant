"""
Hybrid Retrieval-Augmented Generation workflow.

This module orchestrates adaptive retrieval,
cross-source reranking, context fusion,
and answer generation.
"""

from langchain_chroma import Chroma

from config.settings import HYBRID_TOP_K
from models.confidence import Confidence
from models.ranked_candidate import RankedCandidate
from models.response import Response
from models.retrieval_candidate import RetrievalCandidate
from models.retrieval_strategy import RetrievalStrategy
from models.source import Source
from services.candidate_builder import (
    build_pdf_candidates,
    build_web_candidates,
)
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
from services.retrieval_strategy import (
    determine_retrieval_strategy,
)
from services.retriever import retrieve_documents
from services.web_search import retrieve_from_web


def _rank_candidates(
    question: str,
    candidates: list[RetrievalCandidate],
) -> list[RankedCandidate]:
    """
    Rerank candidates and retain only
    the strongest hybrid evidence.
    """

    return rerank_candidates(
        question,
        candidates,
    )[:HYBRID_TOP_K]


def _build_response(
    question: str,
    candidates: list[RetrievalCandidate],
    source: Source,
    confidence: Confidence,
) -> Response:
    """
    Build a final response from retrieval
    candidates.

    Candidates are reranked, fused into
    structured context, and passed to the
    answer generation service.
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


def answer_from_hybrid(
    vector_store: Chroma,
    question: str,
) -> Response:
    """
    Answer a question using adaptive
    hybrid retrieval.

    The workflow:

        1. Retrieves PDF evidence.
        2. Evaluates PDF retrieval quality.
        3. Selects a retrieval strategy.
        4. Retrieves web evidence when needed.
        5. Normalizes retrieval candidates.
        6. Reranks candidates in a common
           embedding space.
        7. Fuses the strongest evidence.
        8. Generates a grounded answer.

    Args:
        vector_store:
            The initialized Chroma vector store.

        question:
            The user's question.

    Returns:
        Final structured response.
    """

    retrieved_documents = retrieve_documents(
        vector_store,
        question,
    )

    pdf_evaluation = evaluate_pdf_retrieval(
        retrieved_documents,
    )

    strategy = determine_retrieval_strategy(
        pdf_evaluation,
    )

    if strategy is RetrievalStrategy.PDF_ONLY:
        pdf_candidates = build_pdf_candidates(
            retrieved_documents,
        )

        return _build_response(
            question=question,
            candidates=pdf_candidates,
            source=Source.PDF,
            confidence=pdf_evaluation.confidence,
        )

    web_results = retrieve_from_web(
        question,
    )

    web_evaluation = evaluate_web_retrieval(
        web_results,
    )

    if not web_evaluation.passed:
        if strategy is RetrievalStrategy.HYBRID:
            pdf_candidates = build_pdf_candidates(
                retrieved_documents,
            )

            return _build_response(
                question=question,
                candidates=pdf_candidates,
                source=Source.PDF,
                confidence=pdf_evaluation.confidence,
            )

        return Response.empty()

    web_candidates = build_web_candidates(
        web_results,
    )

    if strategy is RetrievalStrategy.WEB_ONLY:
        return _build_response(
            question=question,
            candidates=web_candidates,
            source=Source.WEB,
            confidence=web_evaluation.confidence,
        )

    pdf_candidates = build_pdf_candidates(
        retrieved_documents,
    )

    hybrid_candidates = pdf_candidates + web_candidates

    confidence = combine_confidence(
        pdf_evaluation.confidence,
        web_evaluation.confidence,
    )

    return _build_response(
        question=question,
        candidates=hybrid_candidates,
        source=Source.HYBRID,
        confidence=confidence,
    )
