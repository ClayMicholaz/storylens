import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="Apple announced a new AI chip today.",
    config={
        "output_dimensionality": 768,
    },
)

embedding = result.embeddings[0].values

print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])