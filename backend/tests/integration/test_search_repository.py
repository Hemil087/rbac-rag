from app.db.repositories.search_repository import search_similar_chunks
from app.rag.embeddings import generate_embedding


def test_employee_can_retrieve_authorized_document(db_session):
    query_embedding = generate_embedding(
        "What is explained in the engineering handbook?"
    )

    results = search_similar_chunks(
        db=db_session,
        query_embedding=query_embedding,
        org_id=1,
        role_id=3,
        top_k=5,
    )

    assert len(results) > 0

    for chunk, distance in results:
        assert chunk.doc_id == 2


def test_employee_cannot_retrieve_restricted_acme_documents(db_session):
    query_embedding = generate_embedding(
        "What is the HR policy?"
    )

    results = search_similar_chunks(
        db=db_session,
        query_embedding=query_embedding,
        org_id=1,
        role_id=3,
        top_k=5,
    )

    returned_doc_ids = {chunk.doc_id for chunk, distance in results}

    assert 1 not in returned_doc_ids
    assert 3 not in returned_doc_ids


def test_acme_employee_cannot_retrieve_globex_documents(db_session):
    query_embedding = generate_embedding(
        "What is the Globex finance policy?"
    )

    results = search_similar_chunks(
        db=db_session,
        query_embedding=query_embedding,
        org_id=1,
        role_id=3,
        top_k=5,
    )

    returned_doc_ids = {chunk.doc_id for chunk, distance in results}

    assert 4 not in returned_doc_ids
    assert 5 not in returned_doc_ids