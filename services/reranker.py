"""
Cross-source reranking service.

This module reranks retrieval candidates
using a common embedding space.
"""

import math

from models.ranked_candidate import RankedCandidate
from models.retrieval_candidate import RetrievalCandidate
from services.embeddings import embeddings


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """
    Calculate cosine similarity between
    two embedding vectors.

    Args:
        vector_a:
            First embedding vector.

        vector_b:
            Second embedding vector.

    Returns:
        Cosine similarity between the vectors.
    """

    dot_product = sum(
        a * b
        for a, b in zip(
            vector_a,
            vector_b,
            strict=True,
        )
    )

    magnitude_a = math.sqrt(sum(value * value for value in vector_a))

    magnitude_b = math.sqrt(sum(value * value for value in vector_b))

    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def rerank_candidates(
    question: str,
    candidates: list[RetrievalCandidate],
) -> list[RankedCandidate]:
    """
    Rerank retrieval candidates against
    the user's question.

    All candidates are embedded using the
    same embedding model so PDF and web
    content can be compared in a common
    semantic space.

    Args:
        question:
            The user's question.

        candidates:
            Retrieval candidates from one
            or more knowledge sources.

    Returns:
        Candidates ordered from most to
        least relevant.
    """

    if not candidates:
        return []

    question_embedding = embeddings.embed_query(
        question,
    )

    candidate_embeddings = embeddings.embed_documents(
        [candidate.content for candidate in candidates]
    )

    ranked_candidates = [
        RankedCandidate(
            candidate=candidate,
            relevance_score=cosine_similarity(
                question_embedding,
                candidate_embedding,
            ),
        )
        for candidate, candidate_embedding in zip(
            candidates,
            candidate_embeddings,
            strict=True,
        )
    ]

    return sorted(
        ranked_candidates,
        key=lambda candidate: candidate.relevance_score,
        reverse=True,
    )
