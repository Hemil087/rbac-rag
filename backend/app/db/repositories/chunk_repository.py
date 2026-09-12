from sqlalchemy.orm import Session

from app.db.models import DocumentChunk


def create_document_chunks(
    db: Session,
    doc_id: int,
    chunks: list[str],
    embeddings: list[list[float]],
):
    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match")

    document_chunks = [
        DocumentChunk(
            doc_id=doc_id,
            chunk_index=index,
            chunk_text=chunk,
            embedding=embedding,
            chunk_metadata={},
        )
        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    db.add_all(document_chunks)
    db.commit()

    return document_chunks