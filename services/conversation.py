"""
Conversation orchestration service.

This module coordinates conversation memory,
context-aware question rewriting, retrieval,
and memory updates.
"""

from langchain_chroma import Chroma

from models.response import Response
from services.conversation_memory import ConversationMemory
from services.question_rewriter import rewrite_question
from services.router import route_question


class ConversationService:
    """
    Orchestrate context-aware conversational
    interactions with the retrieval pipeline.
    """

    def __init__(
        self,
        vector_store: Chroma,
        memory: ConversationMemory,
    ) -> None:
        """
        Initialize the conversation service.

        Args:
            vector_store:
                The initialized Chroma vector store.

            memory:
                Conversation memory for the
                current application session.
        """

        self._vector_store = vector_store
        self._memory = memory

    def ask(
        self,
        question: str,
    ) -> Response | None:
        """
        Process a conversational question.

        The question is resolved against recent
        conversation history before being routed
        through the retrieval pipeline.

        Args:
            question:
                The user's original question.

        Returns:
            The generated response when the
            question can be resolved.

            None when additional conversational
            context is required.
        """

        rewrite_result = rewrite_question(
            question,
            self._memory.messages,
        )

        if not rewrite_result.resolved:
            return None

        response = route_question(
            self._vector_store,
            rewrite_result.question,
        )

        self._memory.add_user_message(
            question,
        )

        self._memory.add_assistant_message(
            response.answer,
        )

        return response

    def clear(self) -> None:
        """
        Clear the current conversation history.
        """

        self._memory.clear()
