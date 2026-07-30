"""
Web Retrieval-Augmented Generation workflow.
"""

from models.citation import Citation
from models.response import Response
from models.source import Source
from services.evaluator import (
    evaluate_web_retrieval,
)
from services.generator import (
    build_context,
    generate_answer,
)
from services.web_search import (
    retrieve_from_web,
)


def answer_from_web(
    question: str,
) -> Response:
    """
    Answer a user's question using
    web search.
    """

    results = retrieve_from_web(
        question,
    )

    evaluation = evaluate_web_retrieval(
        results,
    )

    if not evaluation.passed:
        return Response.empty()

    context = build_context([result.content for result in results])

    seen = set()
    citations = []

    for result in results:
        if result.url in seen:
            continue

        seen.add(result.url)

        citations.append(
            Citation(
                title=result.title,
                location="Web",
                url=result.url,
            )
        )

    return Response(
        answer=generate_answer(
            context,
            question,
        ),
        source=Source.WEB,
        confidence=evaluation.confidence,
        citations=citations,
    )
