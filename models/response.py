"""
Response model.
"""

from dataclasses import dataclass

from models.citation import Citation
from models.confidence import Confidence
from models.source import Source

NOT_FOUND_MESSAGE = "I couldn't find relevant information to answer your question."


@dataclass(slots=True)
class Response:
    """
    Final response returned to the user.
    """

    answer: str
    source: Source
    confidence: Confidence
    citations: list[Citation]

    @property
    def found(self) -> bool:
        """
        Whether the response contains
        a valid answer.
        """
        return self.source is not Source.NONE

    @classmethod
    def empty(cls) -> "Response":
        return cls(
            answer=NOT_FOUND_MESSAGE,
            source=Source.NONE,
            confidence=Confidence.NONE,
            citations=[],
        )
