"""
Agent service.

This module orchestrates question
answering for the AI agent.
"""

from langchain_chroma import Chroma

from models.agent_state import AgentState
from models.response import Response
from models.tool_runtime import ToolRuntime
from services.agent_planner import (
    create_tool_calls,
)
from services.hybrid_workflow import (
    execute_hybrid_workflow,
)
from services.tool_executor import (
    execute_tool,
)


def answer_question(
    vector_store: Chroma,
    question: str,
) -> Response:
    """
    Answer a user question.

    Currently the agent executes
    planned tools before delegating
    to the existing hybrid workflow.
    This enables gradual migration
    toward a fully agentic pipeline.

    Args:
        vector_store:
            The initialized Chroma
            vector store.

        question:
            User question.

    Returns:
        Final structured response.
    """

    state = AgentState(
        question=question,
    )

    state.tool_calls = create_tool_calls(
        state.question,
    )

    runtime = ToolRuntime(
        vector_store=vector_store,
    )

    state.tool_results = tuple(
        execute_tool(
            tool_call,
            runtime,
        )
        for tool_call in state.tool_calls
    )

    # Temporary until the agent owns
    # the complete response pipeline.
    _ = state

    return execute_hybrid_workflow(
        vector_store,
        state.question,
    )
