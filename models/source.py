"""
Response source model.
"""

from enum import Enum


class Source(Enum):
    """
    Supported answer sources.
    """

    PDF = "PDF"
    WEB = "Web"
    HYBRID = "Hybrid"
    NONE = "None"
