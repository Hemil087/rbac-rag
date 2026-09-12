from app.rag.embeddings import (
    generate_embedding,
    generate_embeddings,
)


def test_embedding_dimension():

    text = "Employees receive annual leave."

    embedding = generate_embedding(text)

    assert len(embedding) == 384


def test_embedding_contains_numbers():

    embedding = generate_embedding(
        "This is a test document."
    )

    assert all(
        isinstance(value, float)
        for value in embedding
    )


def test_batch_embeddings():

    texts = [
        "Annual leave policy.",
        "Employee benefits.",
        "Engineering handbook.",
    ]

    embeddings = generate_embeddings(texts)

    assert len(embeddings) == 3

    assert all(
        len(embedding) == 384
        for embedding in embeddings
    )


def test_similar_texts_are_more_similar():

    from sentence_transformers.util import cos_sim

    text1 = "Employees receive annual leave."
    text2 = "Workers are entitled to vacation days."
    text3 = "The company uses PostgreSQL."

    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)
    embedding3 = generate_embedding(text3)

    similarity_related = cos_sim(
        embedding1,
        embedding2,
    ).item()

    similarity_unrelated = cos_sim(
        embedding1,
        embedding3,
    ).item()

    assert similarity_related > similarity_unrelated