from app.services.rag_service import retrieve_context


def test_retrieve_context_for_authorized_user(db_session):
    results = retrieve_context(
        db=db_session,
        question="What is a structure?",
        org_id=1,
        role_id=3,
        top_k=5,
    )

    assert len(results) > 0

    for result in results:
        assert "chunk_id" in result
        assert "document_id" in result
        assert "chunk_index" in result
        assert "text" in result
        assert "distance" in result

        assert result["text"]
        assert result["distance"] >= 0


def test_retrieve_context_rejects_empty_question(db_session):
    try:
        retrieve_context(
            db=db_session,
            question="   ",
            org_id=1,
            role_id=3,
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "Question cannot be empty"