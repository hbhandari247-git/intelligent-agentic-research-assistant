"""
Answer generation service.

This module builds the retrieval context
and generates answers using the language model.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from services.llm import llm

PROMPT = """
You are a helpful research assistant.

Use ONLY the provided context to answer the user's question.

Combine information from multiple context sections into a single, coherent answer whenever appropriate.

Do NOT use outside knowledge, make assumptions, or fabricate information.

If the context does not contain enough information to answer the question, respond exactly with:

"I don't have enough information to answer this question based on the available context."

Context:
{context}

Question:
{question}

Answer:
"""


prompt = PromptTemplate(
    template=PROMPT,
    input_variables=[
        "context",
        "question",
    ],
)

generation_chain = prompt | llm | StrOutputParser()


def build_context(
    chunks: list[str],
) -> str:
    """
    Create a single context string
    from retrieved text chunks.
    """

    return "\n\n".join(chunks)


def generate_answer(
    context: str,
    question: str,
) -> str:
    """
    Generate an answer using
    the configured language model.
    """

    return generation_chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )
