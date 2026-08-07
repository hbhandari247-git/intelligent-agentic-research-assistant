"""
Tool executor service.

This module executes tool calls
created by the AI agent.
"""

from collections.abc import Callable

from models.tool import Tool
from models.tool_call import ToolCall
from models.tool_result import ToolResult
from models.tool_runtime import ToolRuntime
from services.tool_registry import (
    SEARCH_PDF_TOOL,
    SEARCH_WEB_TOOL,
)
from services.tools.pdf_tool import (
    execute_pdf_tool,
)
from services.tools.web_tool import (
    execute_web_tool,
)

ToolExecutor = Callable[
    [ToolCall, ToolRuntime],
    ToolResult,
]


def execute_tool(
    tool_call: ToolCall,
    runtime: ToolRuntime,
) -> ToolResult:
    """
    Execute a tool call.

    Args:
        tool_call:
            Tool invocation requested
            by the AI agent.

        runtime:
            Runtime resources available
            to tool execution.

    Returns:
        Tool execution result.

    Raises:
        ValueError:
            If the requested tool
            is unknown.
    """

    executor = TOOL_EXECUTORS.get(
        tool_call.tool,
    )

    if executor is None:
        raise ValueError(f"Unknown tool: " f"'{tool_call.tool.name}'.")

    return executor(
        tool_call,
        runtime,
    )


TOOL_EXECUTORS: dict[
    Tool,
    ToolExecutor,
] = {
    SEARCH_PDF_TOOL: execute_pdf_tool,
    SEARCH_WEB_TOOL: execute_web_tool,
}
