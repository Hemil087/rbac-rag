from pathlib import Path

import fitz


def load_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported"
        )

    document = fitz.open(file_path)

    pages = []

    try:
        for page in document:
            text = page.get_text()

            if text.strip():
                pages.append(text)

    finally:
        document.close()

    return "\n".join(pages)