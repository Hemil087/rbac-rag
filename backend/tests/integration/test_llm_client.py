from app.llm.llm_client import generate_answer


def test_generate_answer():
    answer = generate_answer(
        question="What is 2 + 2?",
        context="Basic arithmetic tells us that 2 + 2 = 4.",
    )

    assert answer
    assert isinstance(answer, str)