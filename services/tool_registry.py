"""
Tool registry service.

This module defines the tools
available to the AI agent.
"""

from models.tool import Tool

SEARCH_PDF_TOOL = Tool(
    name="search_pdf",
    description=("Search the local knowledge base " "for relevant information."),
)

SEARCH_WEB_TOOL = Tool(
    name="search_web",
    description=("Search the web for current " "or external information."),
)

TOOLS = (
    SEARCH_PDF_TOOL,
    SEARCH_WEB_TOOL,
)


def list_tools() -> tuple[Tool, ...]:
    """
    Return all available tools.
    """

    return TOOLS
