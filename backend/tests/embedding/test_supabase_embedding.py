import os
import json

from dotenv import load_dotenv
from google import genai
from supabase import create_client


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


# ============================================================
# Validate environment variables
# ============================================================

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing")

if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY is missing")


# ============================================================
# Create clients
# ============================================================

gemini = genai.Client(
    api_key=GOOGLE_API_KEY
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


# ============================================================
# 1. Get an existing article from Supabase
# ============================================================

response = (
    supabase
    .table("articles")
    .select("id, title, summary")
    .limit(1)
    .execute()
)

if not response.data:
    raise ValueError("No articles found in the database")

article = response.data[0]

print("\n1. Article retrieved")
print("ID:", article["id"])
print("Title:", article["title"])


# ============================================================
# 2. Combine title + summary
# ============================================================

title = article["title"] or ""
summary = article["summary"] or ""

text = f"{title}. {summary}"

print("\n2. Text to embed")
print(text)


# ============================================================
# 3. Generate embedding with Gemini
# ============================================================

result = gemini.models.embed_content(
    model="gemini-embedding-2",
    contents=text,
    config={
        "output_dimensionality": 768,
    },
)

embedding = result.embeddings[0].values

print("\n3. Gemini embedding generated")
print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])

if len(embedding) != 768:
    raise ValueError(
        f"Gemini returned {len(embedding)} dimensions instead of 768"
    )


# ============================================================
# 4. Update the article in Supabase
# ============================================================

update_response = (
    supabase
    .table("articles")
    .update({
        "embedding": embedding
    })
    .eq("id", article["id"])
    .execute()
)

print("\n4. Article updated")
print("Updated rows:", len(update_response.data))


# ============================================================
# 5. Read the embedding back from Supabase
# ============================================================

response = (
    supabase
    .table("articles")
    .select("id, embedding")
    .eq("id", article["id"])
    .single()
    .execute()
)

saved_embedding = response.data["embedding"]


# ============================================================
# 6. Convert Supabase's vector string back into a Python list
# ============================================================

if isinstance(saved_embedding, str):
    saved_embedding = json.loads(saved_embedding)


# ============================================================
# 7. Verify
# ============================================================

print("\n5. Embedding retrieved from Supabase")
print("Saved embedding type:", type(saved_embedding))
print("Saved embedding length:", len(saved_embedding))
print("First 5 saved values:", saved_embedding[:5])

if len(saved_embedding) != 768:
    raise ValueError(
        f"Expected 768 dimensions, got {len(saved_embedding)}"
    )


# ============================================================
# 8. Compare first few values
# ============================================================

print("\n6. Comparing Gemini vs Supabase")

print("Gemini first 5:")
print(embedding[:5])

print("\nSupabase first 5:")
print(saved_embedding[:5])


# ============================================================
# Final result
# ============================================================

print("\n" + "=" * 60)
print("✅ SUCCESS")
print("Gemini → 768-dimensional embedding → Supabase")
print("=" * 60)