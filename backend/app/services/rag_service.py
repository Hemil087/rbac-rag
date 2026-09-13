from sqlalchemy.orm import Session

from app.db.repositories.search_repository import search_similar_chunks
from app.rag.embeddings import generate_embedding
from app.llm.llm_client import generate_answer as call_llm


def retrieve_context(
    db: Session,
    question: str,
    org_id: int,
    role_id: int,
    top_k: int = 5,
):
    if not question.strip():
        raise ValueError("Question cannot be empty")

    query_embedding = generate_embedding(question)

    results = search_similar_chunks(
        db=db,
        query_embedding=query_embedding,
        org_id=org_id,
        role_id=role_id,
        top_k=top_k,
    )

    return [
        {
            "chunk_id": chunk.id,
            "document_id": chunk.doc_id,
            "chunk_index": chunk.chunk_index,
            "text": chunk.chunk_text,
            "distance": float(distance),
        }
        for chunk, distance in results
    ]


def generate_rag_answer(
    db: Session,
    question: str,
    org_id: int,
    role_id: int,
    conversation_history: list[dict] | None = None,
    top_k: int = 5,
):
    context_chunks = retrieve_context(
        db=db,
        question=question,
        org_id=org_id,
        role_id=role_id,
        top_k=top_k,
    )

    if not context_chunks:
        return (
            "I could not find any relevant information "
            "in the documents you have access to."
        ), []

    context = "\n\n".join(
        [
            (
                f"[Document {chunk['document_id']}, "
                f"Chunk {chunk['chunk_index']}]\n"
                f"{chunk['text']}"
            )
            for chunk in context_chunks
        ]
    )

    answer = call_llm(
        question=question,
        context=context,
        conversation_history=conversation_history,
    )

    sources = [
        {
            "document_id": chunk["document_id"],
            "chunk_id": chunk["chunk_id"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in context_chunks
    ]

    return answer, sources