import pytest

from app.ingestion.pipeline import (
    make_article_hash,
    make_content_hash,
    normalize_articles,
)


class TestMakeArticleHash:
    def test_deterministic(self):
        """Same URL + title always produces the same hash."""
        h1 = make_article_hash("https://example.com/article", "Test Title")
        h2 = make_article_hash("https://example.com/article", "Test Title")
        assert h1 == h2

    def test_different_urls_different_hashes(self):
        """Different URLs produce different hashes."""
        h1 = make_article_hash("https://example.com/article-1", "Same Title")
        h2 = make_article_hash("https://example.com/article-2", "Same Title")
        assert h1 != h2

    def test_different_titles_different_hashes(self):
        """Different titles produce different hashes."""
        h1 = make_article_hash("https://example.com/article", "Title One")
        h2 = make_article_hash("https://example.com/article", "Title Two")
        assert h1 != h2

    def test_whitespace_stripping(self):
        """Leading/trailing whitespace is stripped before hashing."""
        h1 = make_article_hash("  https://example.com/article  ", "  Test Title  ")
        h2 = make_article_hash("https://example.com/article", "Test Title")
        assert h1 == h2


class TestMakeContentHash:
    def test_deterministic(self):
        """Same content always produces the same hash."""
        c1 = make_content_hash("Full article content here.")
        c2 = make_content_hash("Full article content here.")
        assert c1 == c2

    def test_empty_content(self):
        """Empty or None content produces a hash (doesn't crash)."""
        h1 = make_content_hash("")
        h2 = make_content_hash(None)
        assert isinstance(h1, str) and len(h1) == 64
        assert isinstance(h2, str) and len(h2) == 64

    def test_different_content_different_hashes(self):
        """Different content produces different hashes."""
        c1 = make_content_hash("Content A")
        c2 = make_content_hash("Content B")
        assert c1 != c2


class TestNormalizeArticles:
    def test_normalize_adds_hashes(self):
        """Normalize adds article_hash and content_hash to each article."""
        articles = [
            {"url": "https://example.com/a1", "title": "Article 1", "content": "Some content"},
            {"url": "https://example.com/a2", "title": "Article 2", "content": "More content"},
        ]
        result = normalize_articles(articles)
        assert len(result) == 2
        assert "article_hash" in result[0]
        assert "content_hash" in result[0]
        assert "article_hash" in result[1]
        assert "content_hash" in result[1]

    def test_skips_missing_url(self):
        """Articles without a URL are skipped."""
        articles = [
            {"url": "", "title": "No URL", "content": "Content"},
            {"url": "https://example.com/valid", "title": "Valid", "content": "Content"},
        ]
        result = normalize_articles(articles)
        assert len(result) == 1
        assert result[0]["title"] == "Valid"

    def test_skips_missing_title(self):
        """Articles without a title are skipped."""
        articles = [
            {"url": "https://example.com/a1", "title": "", "content": "Content"},
            {"url": "https://example.com/a2", "title": "Valid Title", "content": "Content"},
        ]
        result = normalize_articles(articles)
        assert len(result) == 1
        assert result[0]["url"] == "https://example.com/a2"

    def test_preserves_all_fields(self):
        """Normalize preserves original fields and adds hash fields."""
        article = {
            "url": "https://example.com/article",
            "title": "Test Article",
            "summary": "Summary text",
            "content": "Full content",
            "source": "Test Source",
            "category": "tech",
            "published_date": "2025-06-15T10:00:00Z",
        }
        result = normalize_articles([article])
        assert len(result) == 1
        normalized = result[0]
        assert normalized["title"] == "Test Article"
        assert normalized["source"] == "Test Source"
        assert normalized["category"] == "tech"
        assert normalized["url"] == "https://example.com/article"