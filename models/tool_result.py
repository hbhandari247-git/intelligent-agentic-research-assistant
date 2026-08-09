"""
Tool result model.

Represents the result produced after
the AI agent executes a tool.
"""

from dataclasses import dataclass
from typing import Any

from models.knowledge import Knowledge
from models.tool import Tool


@dataclass(slots=True, frozen=True)
class ToolResult:
    """
    Result produced by a tool execution.
    """

    tool: Tool

    arguments: dict[str, Any]

    knowledge: Knowledge | None = None

    success: bool = True

    error: str | None = None

    @property
    def has_relevant_content(self) -> bool:
        """
        Return whether the tool produced
        usable retrieval content.
        """

        if not self.success:
            return False

        if self.knowledge is None:
            return False

        return any(
            candidate.content.strip()
            for candidate in self.knowledge.candidates
            if candidate.content
        )

    @property
    def observation(self) -> str:
        """
        Convert the tool result into text
        for agent observations.
        """

        if not self.success:
            return (
                f"Tool '{self.tool.name}' failed. "
                f"Error: {self.error or 'Unknown error.'}"
            )

        if self.knowledge is None:
            return (
                f"Tool '{self.tool.name}' completed "
                "successfully but returned no knowledge."
            )

        contents = [
            candidate.content.strip()
            for candidate in self.knowledge.candidates
            if candidate.content and candidate.content.strip()
        ]

        if not contents:
            return (
                f"Tool '{self.tool.name}' completed "
                "successfully but returned no relevant "
                "content."
            )

        return "\n\n".join(contents)
