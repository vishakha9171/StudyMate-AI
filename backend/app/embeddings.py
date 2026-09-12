from google import genai

from .config import (
    GEMINI_API_KEY,
    GEMINI_EMBEDDING_MODEL,
)

client = genai.Client(api_key=GEMINI_API_KEY)


def create_embedding(text):
    result = client.models.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        contents=text,
        config={
            "output_dimensionality": 768
        }
    )

    return result.embeddings[0].values


def create_embeddings(texts):
    if not texts:
        return []

    embeddings = []

    for text in texts:
        embedding = create_embedding(text)
        embeddings.append(embedding)

    return embeddings