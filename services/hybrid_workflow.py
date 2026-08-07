"""
Hybrid workflow.

This module executes the hybrid
knowledge retrieval workflow for
the AI agent.
"""

from langchain_chroma import Chroma

from models.response import Response
from models.retrieval_strategy import RetrievalStrategy
from models.source import Source
from services.evaluator import (
    combine_confidence,
    evaluate_pdf_retrieval,
    evaluate_web_retrieval,
)
from services.knowledge.pdf import (
    search_pdf_knowledge,
)
from services.knowledge.web import (
    search_web_knowledge,
)
from services.response_builder import (
    build_response,
)
from services.retrieval_strategy import (
    determine_retrieval_strategy,
)


def execute_hybrid_workflow(
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
        5. Reranks candidates in a common
           embedding space.
        6. Fuses the strongest evidence.
        7. Generates a grounded answer.

    Args:
        vector_store:
            The initialized Chroma vector store.

        question:
            The user's question.

    Returns:
        Final structured response.
    """

    pdf_knowledge = search_pdf_knowledge(
        vector_store,
        question,
    )

    pdf_candidates = pdf_knowledge.candidates

    pdf_evaluation = evaluate_pdf_retrieval(
        pdf_knowledge.retrieved_documents,
    )

    strategy = determine_retrieval_strategy(
        pdf_evaluation,
    )

    if strategy is RetrievalStrategy.PDF_ONLY:
        return build_response(
            question=question,
            candidates=pdf_candidates,
            source=Source.PDF,
            confidence=pdf_evaluation.confidence,
        )

    web_knowledge = search_web_knowledge(
        question,
    )

    web_candidates = web_knowledge.candidates

    web_evaluation = evaluate_web_retrieval(
        web_knowledge.results,
    )

    if not web_evaluation.passed:
        if strategy is RetrievalStrategy.HYBRID:
            return build_response(
                question=question,
                candidates=pdf_candidates,
                source=Source.PDF,
                confidence=pdf_evaluation.confidence,
            )

        return Response.empty()

    if strategy is RetrievalStrategy.WEB_ONLY:
        return build_response(
            question=question,
            candidates=web_candidates,
            source=Source.WEB,
            confidence=web_evaluation.confidence,
        )

    hybrid_candidates = pdf_candidates + web_candidates

    confidence = combine_confidence(
        pdf_evaluation.confidence,
        web_evaluation.confidence,
    )

    return build_response(
        question=question,
        candidates=hybrid_candidates,
        source=Source.HYBRID,
        confidence=confidence,
    )
