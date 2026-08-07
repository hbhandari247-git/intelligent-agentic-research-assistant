"""
Agent state model.

Represents the current state of
the AI agent while answering a
question.
"""

from dataclasses import dataclass

from models.tool_call import ToolCall
from models.tool_result import ToolResult


@dataclass(slots=True)
class AgentState:
    """
    Current state of the AI agent.
    """

    question: str

    tool_calls: tuple[ToolCall, ...] = ()

    tool_results: tuple[ToolResult, ...] = ()
