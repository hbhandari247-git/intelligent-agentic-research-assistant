"""
Tool result model.
"""

from dataclasses import dataclass

from models.knowledge import Knowledge
from models.tool import Tool


@dataclass(slots=True, frozen=True)
class ToolResult:
    """
    Represents the result returned
    by a tool.
    """

    tool: Tool

    knowledge: Knowledge
