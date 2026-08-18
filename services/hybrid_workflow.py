"""
Hybrid workflow.

This module executes the hybrid
knowledge retrieval workflow for
the AI agent.

This workflow is retained as a
standalone retrieval workflow.
The primary agent path now uses
the agentic tool execution workflow.
"""

from langchain_chroma import Chroma

from models.response import Response
from models.retrieval_strategy import RetrievalStrategy
from models.tool_result import ToolResult
from services.evaluator import (
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
from services.tool_registry import SEARCH_PDF_TOOL, SEARCH_WEB_TOOL


def execute_hybrid_workflow(
    vector_store: Chroma,
    question: str,
) -> Response:
    """
    Answer a question using adaptive
    hybrid retrieval.

    This workflow is retained as a
    standalone retrieval workflow.

    The primary agent workflow now
    performs tool selection and tool
    execution independently.

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

    pdf_evaluation = evaluate_pdf_retrieval(
        pdf_knowledge.retrieved_documents,
    )

    strategy = determine_retrieval_strategy(
        pdf_evaluation,
    )

    if strategy is RetrievalStrategy.PDF_ONLY:
        return build_response(
            question=question,
            tool_results=(
                ToolResult(
                    tool=SEARCH_PDF_TOOL,
                    arguments={"query": question},
                    knowledge=pdf_knowledge,
                ),
            ),
        )

    web_knowledge = search_web_knowledge(
        question,
    )

    web_evaluation = evaluate_web_retrieval(
        web_knowledge.results,
    )

    if not web_evaluation.passed:
        if strategy is RetrievalStrategy.HYBRID:
            return build_response(
                question=question,
                tool_results=(
                    ToolResult(
                        tool=SEARCH_PDF_TOOL,
                        arguments={"query": question},
                        knowledge=pdf_knowledge,
                    ),
                ),
            )

        return Response.empty()

    if strategy is RetrievalStrategy.WEB_ONLY:
        return build_response(
            question=question,
            tool_results=(
                ToolResult(
                    tool=SEARCH_WEB_TOOL,
                    arguments={"query": question},
                    knowledge=web_knowledge,
                ),
            ),
        )

    return build_response(
        question=question,
        tool_results=(
            ToolResult(
                tool=SEARCH_PDF_TOOL,
                arguments={"query": question},
                knowledge=pdf_knowledge,
            ),
            ToolResult(
                tool=SEARCH_WEB_TOOL,
                arguments={"query": question},
                knowledge=web_knowledge,
            ),
        ),
    )
