"""
Answer generation service.

This module builds the retrieval context
and generates answers using the language model.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from services.llm import llm


PROMPT_TEMPLATE = """
You are a helpful research assistant.

Answer the user's question using ONLY the provided context.

If the answer is not present in the context, say:

"I don't have enough information from the provided document."

Context:
{context}

Question:
{question}

Answer:
"""


prompt_template = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=[
        "context",
        "question",
    ],
)

generation_chain = (
    prompt_template
    | llm
    | StrOutputParser()
)


def build_context(
    chunks: list[str],
) -> str:
    """
    Create a single context string
    from retrieved text chunks.

    Args:
        chunks:
            Retrieved text chunks.

    Returns:
        A single context string for
        the language model.
    """

    return "\n\n".join(chunks)


def generate_answer(
    context: str,
    question: str,
) -> str:
    """
    Generate an answer using
    the configured language model.

    Args:
        context:
            Context built from the
            retrieved text.

        question:
            The user's question.

    Returns:
        The generated answer.
    """

    return generation_chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )