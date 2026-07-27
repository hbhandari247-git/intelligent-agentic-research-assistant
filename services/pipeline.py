"""
Application startup pipeline.

This module prepares everything needed
before the interactive chat loop begins.
"""

from langchain_chroma import Chroma

from config.settings import PDF_PATH
from services.document_loader import load_pdf
from services.text_splitter import split_documents
from services.vector_store import get_vector_store


def initialize_pipeline() -> Chroma:
    """
    Initialize the RAG pipeline.

    Workflow:

        1. Load the PDF.
        2. Split it into chunks.
        3. Create or load the vector database.

    Returns:
        An initialized Chroma vector store.
    """

    print("📄 Loading PDF...")

    documents = load_pdf(PDF_PATH)

    print("✂️ Splitting document into chunks...")

    chunks = split_documents(documents)

    vector_store = get_vector_store(chunks)

    print("✅ Pipeline initialized.\n")

    return vector_store
