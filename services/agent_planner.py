"""
Agent planner service.

This module plans tool invocations
for the AI agent.
"""

from models.tool_call import ToolCall
from services.tool_selector import select_tools


def create_tool_calls(
    question: str,
) -> tuple[ToolCall, ...]:
    """
    Create tool calls for answering
    a user question.

    Args:
        question:
            User question.

    Returns:
        Planned tool calls.
    """

    return tuple(
        ToolCall(
            tool=tool,
            query=question,
        )
        for tool in select_tools(
            question,
        )
    )
