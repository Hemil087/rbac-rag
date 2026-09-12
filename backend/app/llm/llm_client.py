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
) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful enterprise knowledge assistant. "
                    "Answer the user's question using only the provided "
                    "context. If the answer cannot be found in the "
                    "context, say that you do not have enough information "
                    "to answer. Do not invent facts."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n\n{context}\n\n"
                    f"Question:\n\n{question}"
                ),
            },
        ],
    )

    return response.choices[0].message.content