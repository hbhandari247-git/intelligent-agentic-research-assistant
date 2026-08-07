"""
Tool selector service.

This module selects the most
appropriate tools for a user query.
"""

from models.tool import Tool
from services.tool_registry import list_tools


def select_tools(
    question: str,
) -> tuple[Tool, ...]:
    """
    Select the tools appropriate
    for answering a question.

    Args:
        question:
            User question.

    Returns:
        Selected tools.
    """

    _ = question

    return list_tools()
