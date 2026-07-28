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


tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError(
        "TAVILY_API_KEY not found in environment variables."
    )


client = TavilyClient(
    api_key=tavily_api_key,
)


def retrieve_from_web(
    question: str,
) -> list[str]:
    """
    Answer a question using Tavily Search.

    Args:
        question:
            The user's question.

    Returns:
        Search results as formatted text.
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
        result["content"]
        for result in results
    ]