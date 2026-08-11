"""
Language model initialization.

This module initializes the application's
language model using the configured settings
and environment variables.

The model configuration is centralized in
config.settings so services do not hardcode
provider or model details.
"""

import os

from langchain_groq import ChatGroq

from config.settings import (
    MODEL_NAME,
    TEMPERATURE,
)


def _get_groq_api_key() -> str:
    """
    Return the configured Groq API key.

    Raises:
        ValueError:
            If GROQ_API_KEY is not configured.
    """

    api_key = os.getenv(
        "GROQ_API_KEY",
    )

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in " "environment variables.")

    return api_key


def _create_llm() -> ChatGroq:
    """
    Create the application's configured
    Groq chat model.
    """

    return ChatGroq(
        model=MODEL_NAME,
        api_key=_get_groq_api_key(),
        temperature=TEMPERATURE,
    )


llm = _create_llm()
