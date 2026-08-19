import time

from dotenv import load_dotenv

load_dotenv()

from supabase import create_client
import os

from app.embeddings.service import embedding_service


# ============================================================
# Configuration
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

REQUEST_DELAY = 0.2


# ============================================================
# Validate environment variables
# ============================================================

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing")

if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_SERVICE_ROLE_KEY is missing")


# ============================================================
# Create Supabase client
# ============================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


# ============================================================
# Get articles without embeddings
# ============================================================

def get_articles_without_embeddings():
    response = (
        supabase
        .table("articles")
        .select("id, title, summary")
        .is_("embedding", "null")
        .execute()
    )

    return response.data


# ============================================================
# Save embedding
# ============================================================

def save_embedding(article_id: str, embedding: list[float]):
    response = (
        supabase
        .table("articles")
        .update({
            "embedding": embedding
        })
        .eq("id", article_id)
        .execute()
    )

    if not response.data:
        raise ValueError(
            f"Failed to update article {article_id}"
        )


# ============================================================
# Main
# ============================================================

def main():
    print("Fetching articles without embeddings...")

    articles = get_articles_without_embeddings()

    total = len(articles)

    print(f"Found {total} articles without embeddings.")

    if total == 0:
        print("Nothing to do.")
        return

    successful = 0
    failed = 0

    for index, article in enumerate(articles, start=1):
        article_id = article["id"]
        title = article.get("title") or ""
        summary = article.get("summary") or ""

        print(
            f"\n[{index}/{total}] "
            f"Processing: {title[:80]}"
        )

        try:
            # Generate the embedding using our embedding service
            embedding = embedding_service.generate(
                title,
                summary,
            )

            # Save the embedding to Supabase
            save_embedding(
                article_id,
                embedding,
            )

            successful += 1

            print(
                f"✓ Embedded successfully "
                f"({len(embedding)} dimensions)"
            )

        except Exception as error:
            failed += 1

            print(f"✗ Failed: {error}")

        # Wait between Gemini requests
        if index < total:
            time.sleep(REQUEST_DELAY)

    # ========================================================
    # Summary
    # ========================================================

    print("\n" + "=" * 60)
    print("Embedding generation complete")
    print("=" * 60)

    print(f"Total:      {total}")
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")

    if failed:
        print(
            "\nSome articles failed. "
            "Run the script again to retry them."
        )


if __name__ == "__main__":
    main()