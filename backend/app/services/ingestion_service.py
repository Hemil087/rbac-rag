from sqlalchemy.orm import Session

from app.db.repositories.chunk_repository import (
    create_document_chunks,
    delete_document_chunks,
)
from app.rag.chunker import chunk_text
from app.rag.embeddings import generate_embeddings
from app.rag.loaders import load_pdf


def ingest_document(
    db: Session,
    doc_id: int,
    file_path: str,
):
    try:
        # 1. Extract text from document
        text = load_pdf(file_path)

        # 2. Split text into chunks
        chunks = chunk_text(text)

        if not chunks:
            raise ValueError("Document contains no extractable text")

        # 3. Generate embeddings
        embeddings = generate_embeddings(chunks)

        # 4. Remove previous chunks
        #
        # This makes ingestion repeatable.
        # If the same document is ingested again,
        # its old chunks are replaced.
        delete_document_chunks(
            db=db,
            doc_id=doc_id,
        )

        # 5. Store new chunks + embeddings
        document_chunks = create_document_chunks(
            db=db,
            doc_id=doc_id,
            chunks=chunks,
            embeddings=embeddings,
        )

        # 6. Service owns the transaction
        db.commit()

        return document_chunks

    except Exception:
        db.rollback()
        raise