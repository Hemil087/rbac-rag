from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk, DocumentPermission


def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    org_id: int,
    role_id: int,
    top_k: int = 5,
):
    distance = DocumentChunk.embedding.cosine_distance(query_embedding)

    statement = (
        select(
            DocumentChunk,
            distance.label("distance"),
        )
        .join(
            Document,
            Document.id == DocumentChunk.doc_id,
        )
        .join(
            DocumentPermission,
            (
                (DocumentPermission.doc_id == Document.id)
                & (DocumentPermission.org_id == Document.org_id)
            ),
        )
        .where(
            Document.org_id == org_id,
            DocumentPermission.org_id == org_id,
            DocumentPermission.role_id == role_id,
        )
        .order_by(distance)
        .limit(top_k)
    )

    return db.execute(statement).all()