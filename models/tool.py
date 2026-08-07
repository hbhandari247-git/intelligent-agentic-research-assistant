"""
Tool model.

Represents a capability that can be
invoked by the AI agent.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Tool:
    """
    Represents a capability that can
    be invoked by the AI agent.
    """

    name: str
    description: str
