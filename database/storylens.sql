CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title TEXT NOT NULL,
    summary TEXT,
    content TEXT NOT NULL,

    source TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,

    published_date TIMESTAMP WITH TIME ZONE NOT NULL,
    category TEXT,

    article_hash VARCHAR(64) UNIQUE NOT NULL,
    content_hash VARCHAR(64) NOT NULL,

    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector(
            'english',
            coalesce(title, '') || ' ' ||
            coalesce(summary, '') || ' ' ||
            coalesce(content, '')
        )
    ) STORED,

    embedding vector(384),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_articles_published_date
ON articles (published_date DESC);

CREATE INDEX idx_articles_search_vector
ON articles USING gin(search_vector);

CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_articles_modtime
BEFORE UPDATE ON articles
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
