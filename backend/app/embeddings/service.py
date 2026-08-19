import os

from google import genai

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSION = 768


class EmbeddingService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("GOOGLE_API_KEY is missing")

        self.client = genai.Client(api_key=api_key)

    def generate(self, title: str, summary: str) -> list[float]:
        title = title or ""
        summary = summary or ""

        text = f"{title}. {summary}"

        result = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config={
                "output_dimensionality": EMBEDDING_DIMENSION,
            },
        )

        embedding = result.embeddings[0].values

        if len(embedding) != EMBEDDING_DIMENSION:
            raise ValueError(
                f"Expected {EMBEDDING_DIMENSION} dimensions, "
                f"got {len(embedding)}"
            )

        return embedding


embedding_service = EmbeddingService()