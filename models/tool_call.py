"""
Tool call model.

Represents a request made by the
AI agent to invoke a tool.
"""

from dataclasses import dataclass

from models.tool import Tool


@dataclass(slots=True, frozen=True)
class ToolCall:
    """
    Represents a request to invoke
    a tool.
    """

    tool: Tool
    query: str
