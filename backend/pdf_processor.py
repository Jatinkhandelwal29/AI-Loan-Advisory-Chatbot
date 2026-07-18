import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from backend.config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_by_page(pdf_path: str):
    """Returns a list of (page_number, text) tuples."""
    pages = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text("text")
            if text.strip():
                pages.append((i + 1, text))
    return pages


def chunk_pdf(pdf_path: str, filename: str):
    """Extracts and splits a PDF into LangChain Document chunks with metadata."""
    pages = extract_text_by_page(pdf_path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    documents = []
    for page_num, text in pages:
        chunks = splitter.split_text(text)
        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={"source": filename, "page": page_num},
                )
            )
    return documents
