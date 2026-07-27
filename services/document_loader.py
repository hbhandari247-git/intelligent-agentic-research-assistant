"""
PDF document loading service.

This module is responsible for loading PDF
documents into LangChain Document objects.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(pdf_path: str) -> list[Document]:
    """
    Load a PDF file.

    Args:
        pdf_path:
            Path to the PDF document.

    Returns:
        A list of LangChain Document objects.
    """

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    return documents
