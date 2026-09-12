from app.db.models import Document, DocumentChunk
from app.services.ingestion_service import ingest_document


def test_ingest_document(db_session):
    document = (
        db_session.query(Document)
        .filter_by(filename="Lec-1.pdf")
        .first()
    )

    assert document is not None

    chunks = ingest_document(
        db=db_session,
        doc_id=document.id,
        file_path=document.storage_path,
    )

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk.doc_id == document.id
        assert chunk.chunk_text
        assert len(chunk.embedding) == 384