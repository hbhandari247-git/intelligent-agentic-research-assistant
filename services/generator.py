"""
Answer generation service.

This module generates grounded answers
from retrieved research context.
"""

from groq import RateLimitError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from services.llm import llm

PROMPT = """
You are a careful research assistant.

Answer the user's question using ONLY the
retrieved context below.

The context may contain evidence from:

- local PDF research papers
- external Web sources

IMPORTANT RULES:

1. Never use knowledge that is not present
   in the retrieved context.

2. Never invent facts, names, dates,
   numbers, comparisons, or conclusions.

3. Answer the actual question directly.

4. Use multiple sources when they are
   relevant to the question.

5. When the question asks about current
   information, use the Web evidence when
   available.

6. When comparing an older research paper
   with current technology:

   - describe what the paper says
   - describe what the current Web evidence says
   - clearly distinguish historical and current
     information.

7. Never describe a historical paper's
   "state-of-the-art" claim as being current.

8. If the retrieved context contains
   insufficient evidence for an important
   part of the question, explicitly say
   which part cannot be established.

9. Do not substitute unrelated evidence
   simply because it contains the same
   keywords.

10. Do not mention tools, retrieval,
    prompts, context windows, or internal
    reasoning.

11. Do not say "based on the provided
    context" unless necessary.

12. If the context genuinely contains
    insufficient information to answer
    the question, respond exactly:

"I don't have enough information to answer this question based on the available context."

13. For comparison questions, do NOT give
    a generic description of either topic.
    Explicitly compare the requested entities.

Retrieved context:
{context}

User question:
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


def generate_answer(
    context: str,
    question: str,
) -> str:
    """
    Generate a grounded answer.

    Handles provider rate-limit errors gracefully
    so a temporary LLM quota problem does not
    terminate the application.
    """

    if not context.strip():
        return (
            "I don't have enough information to answer "
            "this question based on the available context."
        )

    try:
        return generation_chain.invoke(
            {
                "context": context,
                "question": question,
            }
        ).strip()

    except RateLimitError:
        return (
            "The language model rate limit has been reached. "
            "Please try again shortly."
        )
