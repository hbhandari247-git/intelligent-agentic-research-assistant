"""
Language model initialization.

This module initializes the application's
language model using the configured settings
and environment variables.
"""

import os

from langchain_groq import ChatGroq

from config.settings import (
    MODEL_NAME,
    TEMPERATURE,
)


groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables."
    )


llm = ChatGroq(
    model=MODEL_NAME,
    api_key=groq_api_key,
    temperature=TEMPERATURE,
)
