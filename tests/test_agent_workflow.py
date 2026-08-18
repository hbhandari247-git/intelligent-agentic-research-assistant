from unittest.mock import MagicMock, patch

from models.confidence import Confidence
from models.response import Response
from models.source import Source
from models.tool_call import ToolCall
from models.tool_result import ToolResult
from services.agent import answer_question


@patch("services.agent.create_follow_up_tool_calls")
@patch("services.agent.create_tool_calls")
@patch("services.agent.execute_tool")
@patch("services.agent.build_response")
def test_answer_question_loop(mock_build, mock_execute, mock_create, mock_follow_up):
    """
    Verify the agent ReAct loop handles planning, execution, and response steps.
    """
    # Mock planning to return one tool call
    mock_tool = MagicMock()
    mock_tool.name = "search_pdf"
    mock_tool_call = ToolCall(tool=mock_tool, arguments={"query": "test"})
    mock_create.return_value = (mock_tool_call,)
    mock_follow_up.return_value = ()

    from models.knowledge import PDFKnowledge

    # Mock tool execution
    mock_result = ToolResult(
        tool=mock_tool,
        arguments={"query": "test"},
        knowledge=PDFKnowledge(retrieved_documents=[], candidates=[]),
        success=True,
    )
    mock_execute.return_value = mock_result

    # Mock final response construction
    mock_response = Response(
        answer="Mocked answer",
        source=Source.PDF,
        confidence=Confidence.HIGH,
        citations=[],
    )
    mock_build.return_value = mock_response

    mock_vector_store = MagicMock()

    res = answer_question(mock_vector_store, "Test question")

    assert res == mock_response
    mock_create.assert_called_once()
    assert mock_execute.call_count == 1
    args, _kwargs = mock_execute.call_args
    assert args[0] == mock_tool_call
    from models.tool_runtime import ToolRuntime

    assert isinstance(args[1], ToolRuntime)
    mock_build.assert_called_once()
