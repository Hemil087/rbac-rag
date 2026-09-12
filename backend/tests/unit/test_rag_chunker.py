import pytest

from app.rag.chunker import chunk_text


def test_empty_text_returns_no_chunks():

    chunks = chunk_text("")

    assert chunks == []


def test_short_text_returns_one_chunk():

    text = "Hello world"

    chunks = chunk_text(
        text,
        chunk_size=100,
        chunk_overlap=20,
    )

    assert chunks == ["Hello world"]


def test_long_text_is_split():

    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) == 3


def test_chunks_have_overlap():

    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = chunk_text(
        text,
        chunk_size=10,
        chunk_overlap=3,
    )

    assert chunks[0][-3:] == chunks[1][:3]


def test_invalid_overlap():

    with pytest.raises(ValueError):

        chunk_text(
            "hello",
            chunk_size=100,
            chunk_overlap=100,
        )