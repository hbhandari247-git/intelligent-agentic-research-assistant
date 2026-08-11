"""
Tool selector service.

This module determines which registered
tools are required to answer a question.

The planner is intentionally decoupled from
specific tools. Tool capabilities are supplied
dynamically from the tool registry.

The follow-up planner is evidence-aware:
retrieval relevance alone does not imply that
the user's question has been sufficiently answered.
"""

import json
from datetime import datetime, timezone
from typing import Any

from groq import BadRequestError, RateLimitError
from langchain_core.messages import HumanMessage

from models.tool_call import ToolCall
from models.tool_result import ToolResult
from services.llm import llm
from services.tool_registry import (
    get_tool,
    list_tools,
)

# --------------------------------------------------
# Tool catalog
# --------------------------------------------------


def _build_tool_catalog() -> str:
    """
    Build the planner's tool catalog from
    the registered tools.

    No tool names are hardcoded here.
    """

    lines: list[str] = []

    for tool in list_tools():
        arguments = ", ".join(
            tool.arguments,
        )

        lines.append(
            "\n".join(
                (
                    f"Tool: {tool.name}",
                    f"Description: {tool.description}",
                    f"Arguments: {arguments}",
                    ("Selection guidance: " f"{tool.selection_hint}"),
                    f"Scope: {tool.scope}",
                    ("Requires current information: " f"{tool.requires_current}"),
                )
            )
        )

    return "\n\n".join(lines)


# --------------------------------------------------
# Current-question detection
# --------------------------------------------------


def _is_current_question(
    question: str,
) -> bool:
    """
    Determine whether the user explicitly
    requests current or time-sensitive
    information.

    This is only used as a safety constraint
    for current-only tools. It does not decide
    which specific tool should answer the
    question.
    """

    normalized = question.casefold()

    current_terms = (
        "current",
        "currently",
        "latest",
        "today",
        "now",
        "recent",
        "recently",
        "this year",
        "this month",
        "this week",
        "as of",
    )

    return any(term in normalized for term in current_terms)


def _is_comparison_with_current_state(
    question: str,
) -> bool:
    """
    Determine whether the question compares
    something with the current state of a field.

    This is intentionally generic and does not
    reference any specific model, technology,
    company, or domain.
    """

    normalized = question.casefold()

    comparison_terms = (
        "compare",
        "comparison",
        "compared",
        "versus",
        "vs",
        "difference",
        "differences",
        "better than",
        "different from",
    )

    current_state_terms = (
        "current state",
        "state of the art",
        "state-of-the-art",
        "current technology",
        "modern technology",
        "current approaches",
        "modern approaches",
        "current models",
        "modern models",
        "current methods",
        "modern methods",
        "today's",
        "today",
        "latest",
        "currently",
    )

    has_comparison = any(term in normalized for term in comparison_terms)

    has_current_state = any(term in normalized for term in current_state_terms)

    return has_comparison and has_current_state


def _build_current_query(
    question: str,
) -> str:
    """
    Build a concise, search-oriented query for
    tools that require current information.

    The query preserves the user's subject while
    adding generic retrieval dimensions for
    current-state research.
    """

    year = datetime.now(
        timezone.utc,
    ).year

    normalized = " ".join(
        question.strip().split(),
    )

    if _is_comparison_with_current_state(
        normalized,
    ):
        return (
            f"{normalized} {year} "
            "leading approaches "
            "current capabilities "
            "limitations "
            "benchmarks "
            "recent developments"
        )

    if str(year) in normalized:
        return normalized

    return f"{normalized} {year}"


# --------------------------------------------------
# Planner response parsing
# --------------------------------------------------


def _response_to_text(
    response: Any,
) -> str:
    """
    Convert an LLM response into plain text.
    """

    content = getattr(
        response,
        "content",
        response,
    )

    if isinstance(
        content,
        str,
    ):
        return content

    if isinstance(
        content,
        list,
    ):
        parts: list[str] = []

        for item in content:
            if isinstance(
                item,
                str,
            ):
                parts.append(item)

            elif isinstance(
                item,
                dict,
            ):
                text = item.get(
                    "text",
                )

                if text:
                    parts.append(
                        str(text),
                    )

        return "".join(parts)

    return str(content)


def _extract_json(
    text: str,
) -> dict[str, Any] | None:
    """
    Extract a JSON object from planner output.

    The model may occasionally wrap JSON in
    markdown fences, so parsing is intentionally
    tolerant.
    """

    text = text.strip()

    if not text:
        return None

    try:
        parsed = json.loads(
            text,
        )

        if isinstance(
            parsed,
            dict,
        ):
            return parsed

    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    if end <= start:
        return None

    candidate = text[start : end + 1]

    try:
        parsed = json.loads(
            candidate,
        )

    except json.JSONDecodeError:
        return None

    if not isinstance(
        parsed,
        dict,
    ):
        return None

    return parsed


# --------------------------------------------------
# Tool call validation
# --------------------------------------------------


def _convert_tool_calls(
    raw_calls: Any,
) -> tuple[ToolCall, ...]:
    """
    Convert planner JSON into validated
    application ToolCall objects.

    Unknown tools, malformed arguments,
    and incomplete calls are rejected.
    """

    if not isinstance(
        raw_calls,
        list,
    ):
        return ()

    calls: list[ToolCall] = []

    for raw_call in raw_calls:
        if not isinstance(
            raw_call,
            dict,
        ):
            continue

        tool_name = raw_call.get(
            "tool",
        )

        if not isinstance(
            tool_name,
            str,
        ):
            continue

        tool = get_tool(
            tool_name.strip(),
        )

        if tool is None:
            continue

        arguments = raw_call.get(
            "arguments",
        )

        if not isinstance(
            arguments,
            dict,
        ):
            continue

        normalized_arguments: dict[str, Any] = {}

        valid = True

        for argument_name in tool.arguments:
            if argument_name not in arguments:
                valid = False
                break

            value = arguments[argument_name]

            if value is None:
                valid = False
                break

            if isinstance(
                value,
                str,
            ):
                value = value.strip()

                if not value:
                    valid = False
                    break

            normalized_arguments[argument_name] = value

        if not valid:
            continue

        calls.append(
            ToolCall(
                tool=tool,
                arguments=normalized_arguments,
            )
        )

    return tuple(calls)


# --------------------------------------------------
# Current-query normalization
# --------------------------------------------------


def _normalize_current_tool_queries(
    question: str,
    tool_calls: tuple[ToolCall, ...],
) -> tuple[ToolCall, ...]:
    """
    Improve queries for tools that explicitly
    require current information.

    This operates entirely on Tool metadata.

    No specific Web tool or search provider
    is referenced here.
    """

    normalized_calls: list[ToolCall] = []

    for tool_call in tool_calls:
        if not tool_call.tool.requires_current:
            normalized_calls.append(
                tool_call,
            )
            continue

        arguments = dict(
            tool_call.arguments,
        )

        if "query" not in arguments:
            normalized_calls.append(
                tool_call,
            )
            continue

        query = str(
            arguments["query"],
        ).strip()

        if not query:
            normalized_calls.append(
                tool_call,
            )
            continue

        if _is_comparison_with_current_state(
            question,
        ):
            query = _build_current_query(
                question,
            )

        else:
            query = _build_current_query(
                query,
            )

        normalized_calls.append(
            ToolCall(
                tool=tool_call.tool,
                arguments={
                    **arguments,
                    "query": query,
                },
            )
        )

    return tuple(normalized_calls)


# --------------------------------------------------
# Fallback routing
# --------------------------------------------------


def _default_tool_call(
    question: str,
) -> tuple[ToolCall, ...]:
    """
    Provide a safe registry-driven fallback.

    The fallback never assumes that a particular
    tool name is the default local tool.
    """

    tools = list_tools()

    current_tools = [tool for tool in tools if tool.default_for_current]

    local_tools = [tool for tool in tools if tool.default_for_local]

    if _is_current_question(
        question,
    ):
        if current_tools:
            tool = current_tools[0]

        elif local_tools:
            tool = local_tools[0]

        else:
            return ()

    else:
        if local_tools:
            tool = local_tools[0]

        elif tools:
            tool = tools[0]

        else:
            return ()

    if tool.arguments != ("query",):
        return ()

    query = question

    if tool.requires_current:
        query = _build_current_query(
            question,
        )

    return (
        ToolCall(
            tool=tool,
            arguments={
                "query": query,
            },
        ),
    )


# --------------------------------------------------
# Current-only safety filtering
# --------------------------------------------------


def _filter_unnecessary_current_tools(
    question: str,
    tool_calls: tuple[ToolCall, ...],
) -> tuple[ToolCall, ...]:
    """
    Prevent current-only tools from being used
    as supplementary searches when the question
    does not ask for current information and a
    local tool already covers the question.

    This is deliberately generic and operates
    on Tool metadata rather than tool names.
    """

    if _is_current_question(
        question,
    ):
        return tool_calls

    has_local_tool = any(call.tool.scope == "local" for call in tool_calls)

    if not has_local_tool:
        return tool_calls

    return tuple(call for call in tool_calls if not call.tool.requires_current)


# --------------------------------------------------
# Initial planning
# --------------------------------------------------


def select_tool_calls(
    question: str,
) -> tuple[ToolCall, ...]:
    """
    Select the minimum set of registered tools
    required to answer a question.
    """

    question = question.strip()

    if not question:
        return ()

    catalog = _build_tool_catalog()

    prompt = f"""
You are the planning component of an
agentic research assistant.

Your ONLY responsibility is to decide which
registered tools are required to retrieve
evidence for the user's question.

Do NOT answer the question.

Do NOT invent tools.

Do NOT assume tools that are not listed.

TOOL CATALOG
============

{catalog}

ROUTING PRINCIPLES
==================

1. Select the minimum number of tools needed.

2. Prefer local knowledge when the requested
   information is expected to be contained in
   the local knowledge base.

3. Use a current/external tool only when:
   - the user explicitly asks for current,
     latest, recent, today's, now, etc.; OR
   - the required information is genuinely
     external to the local knowledge base.

4. Do NOT add an external/current tool merely
   for confirmation.

5. A comparison with current technology may
   require both historical/local evidence and
   current external evidence.

6. Conversational references have already been
   resolved before reaching this planner.

7. Every selected tool must be registered.

8. Every selected tool must receive all of its
   required arguments.

9. Queries must be specific and self-contained.

10. For current-state questions, make the
    current or external information being
    requested explicit in the query.

11. For comparisons with current technology,
    include both the comparison subject and
    current-state comparison context.

12. Do not return duplicate calls for the same
    tool and arguments.

OUTPUT FORMAT
=============

Return ONLY valid JSON.

Use exactly this structure:

{{
  "tool_calls": [
    {{
      "tool": "registered_tool_name",
      "arguments": {{
        "argument_name": "argument_value"
      }}
    }}
  ]
}}

If no tool is required, return:

{{
  "tool_calls": []
}}

USER QUESTION
=============

{question}
"""

    try:
        response = llm.invoke(
            [
                HumanMessage(
                    content=prompt,
                ),
            ],
        )

    except (BadRequestError, RateLimitError):
        return _default_tool_call(
            question,
        )

    parsed = _extract_json(
        _response_to_text(
            response,
        )
    )

    if parsed is None:
        return _default_tool_call(
            question,
        )

    tool_calls = _convert_tool_calls(
        parsed.get(
            "tool_calls",
            [],
        )
    )

    tool_calls = _normalize_current_tool_queries(
        question,
        tool_calls,
    )

    tool_calls = _filter_unnecessary_current_tools(
        question,
        tool_calls,
    )

    if not tool_calls:
        return _default_tool_call(
            question,
        )

    return tool_calls


# --------------------------------------------------
# Follow-up planning
# --------------------------------------------------


def _format_observations(
    tool_results: tuple[ToolResult, ...],
) -> str:
    """
    Format previous tool results for the
    follow-up planner.
    """

    if not tool_results:
        return "No previous tool results."

    blocks: list[str] = []

    for index, result in enumerate(
        tool_results,
        start=1,
    ):
        blocks.append(
            "\n".join(
                (
                    f"Result {index}",
                    f"Tool: {result.tool.name}",
                    f"Arguments: {result.arguments}",
                    ("Relevant content: " f"{result.has_relevant_content}"),
                    ("Observation:\n" f"{result.observation}"),
                )
            )
        )

    return "\n\n".join(
        blocks,
    )


# --------------------------------------------------
# Follow-up planning
# --------------------------------------------------


def select_follow_up_tool_calls(
    question: str,
    tool_results: tuple[ToolResult, ...],
) -> tuple[ToolCall, ...]:
    """
    Decide whether additional retrieval is needed.

    Retrieval relevance is NOT treated as evidence
    sufficiency.

    The planner evaluates whether the available
    observations actually contain enough information
    to answer the user's question.

    At most one additional retrieval call is
    requested from this function.
    """

    if not tool_results:
        return ()

    catalog = _build_tool_catalog()

    observations = _format_observations(
        tool_results,
    )

    prompt = f"""
You are the evidence-sufficiency component of
an agentic research assistant.

The user asked a question.

One or more retrieval tools have already been
executed.

Your job is NOT to answer the question.

Your job is to decide whether the retrieved
evidence is sufficient to answer the user's
question accurately and directly.

IMPORTANT DISTINCTION
=====================

"Relevant content" does NOT automatically mean
"sufficient evidence".

A result may be relevant but incomplete.

For example, retrieved evidence may:

- mention a concept without defining it;
- state that several items exist without
  identifying all of them;
- contain one part of a multi-part question;
- contain a related fact but not the requested
  fact;
- support a comparison subject but not the
  comparison itself;
- contain an ambiguous or indirect reference;
- contain evidence that requires a more precise
  retrieval query.

Evaluate the actual observation rather than
assuming that a successful retrieval answered
the question.

TOOL CATALOG
============

{catalog}

DECISION RULES
==============

1. If the available evidence directly and
   sufficiently supports the requested answer,
   return an empty tool_calls list.

2. If the evidence is relevant but incomplete,
   request one additional retrieval.

3. If the evidence answers only part of a
   multi-part question, request retrieval for
   the missing part.

4. If the evidence contains a broad statement
   but not the specific supporting details
   needed by the question, refine the query.

5. If another retrieval is unlikely to produce
   meaningful improvement, return an empty list.

6. Prefer the tool that already demonstrated
   useful evidence unless another registered
   tool is clearly required.

7. Use only registered tools.

8. Make at most ONE tool call.

9. Never repeat an identical tool call.

10. The follow-up query must be more specific
    than the previous query when the previous
    evidence was incomplete.

11. The follow-up query should target the
    missing information, not merely repeat the
    original question.

12. Do not use current-only tools unless the
    question actually requires current
    information.

13. Do not search merely to increase the number
    of citations.

14. Do not treat the existence of a relevant
    source as proof that the answer is supported.

OUTPUT FORMAT
=============

Return ONLY valid JSON.

If the evidence is sufficient:

{{
  "tool_calls": []
}}

If another retrieval is justified:

{{
  "tool_calls": [
    {{
      "tool": "registered_tool_name",
      "arguments": {{
        "argument_name": "more_specific_query"
      }}
    }}
  ]
}}

USER QUESTION
=============

{question}

RETRIEVED EVIDENCE
==================

{observations}
"""

    try:
        response = llm.invoke(
            [
                HumanMessage(
                    content=prompt,
                ),
            ],
        )

    except (BadRequestError, RateLimitError):
        return ()

    parsed = _extract_json(
        _response_to_text(
            response,
        )
    )

    if parsed is None:
        return ()

    tool_calls = _convert_tool_calls(
        parsed.get(
            "tool_calls",
            [],
        )
    )

    tool_calls = _normalize_current_tool_queries(
        question,
        tool_calls,
    )

    tool_calls = _filter_unnecessary_current_tools(
        question,
        tool_calls,
    )

    return tool_calls[:1]
