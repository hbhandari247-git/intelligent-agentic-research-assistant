"""
Context-aware question rewriting service.

This module resolves conversational questions
and rewrites them into standalone retrieval
questions.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from models.conversation_message import ConversationMessage
from models.rewrite_result import RewriteResult
from services.llm import llm

REWRITE_PROMPT = """
You are a question rewriting assistant.

Determine whether the user's current question can be understood
using the available conversation history.

If the question depends on missing conversational context,
it is unresolved.

If it can be understood, rewrite it as a standalone question
that can be understood without the conversation history.

Rules:
- Do NOT answer the question.
- Do NOT add new facts.
- Preserve the user's original intent.
- Resolve pronouns and references when the history provides them.
- If the question is already standalone, preserve its meaning.
- If a required reference cannot be resolved, mark it unresolved.

Respond using exactly two lines:

RESOLVED: YES or NO
QUESTION: <standalone question>

Conversation history:
{history}

Current question:
{question}
"""


rewrite_prompt = PromptTemplate(
    template=REWRITE_PROMPT,
    input_variables=[
        "history",
        "question",
    ],
)

rewrite_chain = rewrite_prompt | llm | StrOutputParser()


def build_conversation_history(
    messages: list[ConversationMessage],
) -> str:
    """
    Convert conversation messages into
    text suitable for the rewriting prompt.
    """

    if not messages:
        return "No conversation history."

    return "\n".join(
        f"{message.role.value.capitalize()}: {message.content}" for message in messages
    )


def _parse_rewrite_result(
    output: str,
    original_question: str,
) -> RewriteResult:
    """
    Parse the language model's rewriting
    response into a structured result.
    """

    resolved = None
    rewritten_question = ""

    for line in output.strip().splitlines():
        key, separator, value = line.partition(":")

        if not separator:
            continue

        key = key.strip().upper()
        value = value.strip()

        if key == "RESOLVED":
            resolved = value.upper() == "YES"

        elif key == "QUESTION":
            rewritten_question = value

    if resolved is None:
        return RewriteResult(
            question=original_question,
            resolved=False,
        )

    if not resolved:
        return RewriteResult(
            question=original_question,
            resolved=False,
        )

    return RewriteResult(
        question=rewritten_question or original_question,
        resolved=True,
    )


def rewrite_question(
    question: str,
    messages: list[ConversationMessage],
) -> RewriteResult:
    """
    Resolve and rewrite a conversational
    question for retrieval.

    Args:
        question:
            The user's current question.

        messages:
            Recent conversation history.

    Returns:
        Structured rewrite result containing
        the standalone question and whether
        sufficient context exists.
    """

    history = build_conversation_history(
        messages,
    )

    output = rewrite_chain.invoke(
        {
            "history": history,
            "question": question,
        }
    )

    return _parse_rewrite_result(
        output,
        question,
    )
