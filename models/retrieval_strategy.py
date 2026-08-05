"""
Retrieval strategy model.

This module defines the available
retrieval strategies.
"""

from enum import Enum


class RetrievalStrategy(Enum):
    """
    Available retrieval strategies.
    """

    PDF_ONLY = "PDF Only"
    WEB_ONLY = "Web Only"
    HYBRID = "Hybrid"
