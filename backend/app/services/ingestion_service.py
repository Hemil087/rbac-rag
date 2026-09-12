from sqlalchemy.orm import Session

from app.db.repositories.chunk_repository import create_document_chunks
from app.rag.chunker import chunk_text
from app.rag.embeddings import generate_embeddings
from app.rag.loaders import load_pdf


def ingest_document(
    db: Session,
    doc_id: int,
    file_path: str,
):
    # 1. Extract text from document
    text = load_pdf(file_path)

    # 2. Split text into chunks
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("Document contains no extractable text")

    # 3. Generate embeddings for all chunks
    embeddings = generate_embeddings(chunks)

    # 4. Store chunks + embeddings in PostgreSQL
    document_chunks = create_document_chunks(
        db=db,
        doc_id=doc_id,
        chunks=chunks,
        embeddings=embeddings,
    )

    return document_chunks