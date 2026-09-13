import os

from openai import OpenAI


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not configured")


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def generate_answer(
    question: str,
    context: str,
    conversation_history: list[dict] | None = None,
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful enterprise knowledge assistant. "
                "Answer the user's question using the provided context "
                "and conversation history. "
                "Use only information supported by the context. "
                "If the answer cannot be found in the context, say "
                "that you do not have enough information to answer. "
                "Do not invent facts."
            ),
        }
    ]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append(
        {
            "role": "user",
            "content": (
                f"Context:\n\n{context}\n\n"
                f"Question:\n\n{question}"
            ),
        }
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
    )

    return response.choices[0].message.content