"""
Web search service.

This module provides internet search
capabilities using Tavily Search.
"""

import os

from tavily import TavilyClient

from config.settings import (
    TAVILY_MAX_RESULTS,
)
from models.web_result import WebResult

tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")


client = TavilyClient(
    api_key=tavily_api_key,
)


def retrieve_from_web(
    question: str,
) -> list[WebResult]:
    """
    Retrieve relevant web search results.

    Args:
        question:
            The user's question.

    Returns:
        A list of web search results.
    """

    response = client.search(
        query=question,
        max_results=TAVILY_MAX_RESULTS,
    )

    results = response.get(
        "results",
        [],
    )

    return [
        WebResult(
            title=result.get(
                "title",
                "",
            ),
            url=result.get(
                "url",
                "",
            ),
            content=result.get(
                "content",
                "",
            ),
            score=result.get(
                "score",
                0.0,
            ),
        )
        for result in results
    ]
