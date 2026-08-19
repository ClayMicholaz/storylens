import { API_BASE_URL } from "@/lib/config";
import Link from "next/link";
import { notFound } from "next/navigation";

type Article = {
  id: string;
  title: string;
  summary: string | null;
  source: string;
  category: string;
  url: string;
  published_date: string;
};

type Recommendation = Article & {
  similarity: number;
};

type RecommendationsResponse = {
  data: Recommendation[];
};

async function getArticle(id: string): Promise<Article | null> {
  const res = await fetch(`${API_BASE_URL}/api/articles/${id}`, {
    cache: "no-store",
  });

  if (res.status === 404) {
    return null;
  }

  if (!res.ok) {
    throw new Error("Failed to fetch article");
  }

  return res.json();
}

async function getRecommendations(id: string): Promise<Recommendation[]> {
  const res = await fetch(
    `${API_BASE_URL}/api/articles/${id}/recommendations`,
    {
      cache: "no-store",
    },
  );

  if (!res.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  const data: RecommendationsResponse = await res.json();

  return data.data;
}

type ArticlePageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function ArticlePage({ params }: ArticlePageProps) {
  const { id } = await params;

  const article = await getArticle(id);

  if (!article) {
    notFound();
  }

  const recommendations = await getRecommendations(id);

  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto max-w-4xl px-4 py-8 md:px-6 md:py-12">
        {/* Back */}
        <Link
          href="/"
          className="mb-8 inline-flex items-center text-sm font-medium text-terracotta hover:underline"
        >
          ← Back to stories
        </Link>

        {/* Article */}
        <article>
          <div className="mb-4 flex items-center gap-3">
            <span className="inline-flex rounded-full bg-terracotta/10 px-3 py-1 text-xs font-medium uppercase tracking-wider text-terracotta">
              {article.category}
            </span>

            <span className="text-sm text-muted">
              {new Date(article.published_date).toLocaleDateString()}
            </span>
          </div>

          <h1 className="mb-6 text-3xl font-bold leading-tight text-foreground md:text-5xl">
            {article.title}
          </h1>

          {article.summary && (
            <p className="mb-6 text-lg leading-relaxed text-foreground/70 md:text-xl">
              {article.summary}
            </p>
          )}

          <div className="mb-8 flex items-center justify-between border-b border-terracotta/10 pb-6">
            <span className="font-medium text-pine">{article.source}</span>

            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-lg bg-terracotta px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90"
            >
              Read Original
              <span>↗</span>
            </a>
          </div>
        </article>

        {/* Recommendations */}
        <section className="mt-10">
          <h2 className="mb-5 text-2xl font-bold text-foreground">
            Recommended Stories
          </h2>

          {recommendations.length === 0 ? (
            <p className="text-sm text-muted">No similar stories found.</p>
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {recommendations.map((recommendation) => (
                <article
                  key={recommendation.id}
                  className="rounded-xl border border-terracotta/15 bg-card p-5 transition hover:-translate-y-0.5 hover:shadow-lg hover:shadow-terracotta/5"
                >
                  <div className="mb-3 flex items-center justify-between gap-3">
                    <span className="text-xs font-medium uppercase tracking-wider text-terracotta">
                      {recommendation.category}
                    </span>

                    <span className="text-xs text-muted">
                      {Math.round(recommendation.similarity * 100)}% similar
                    </span>
                  </div>

                  <h3 className="mb-2 text-lg font-bold leading-tight text-foreground">
                    {recommendation.title}
                  </h3>

                  {recommendation.summary && (
                    <p className="mb-4 line-clamp-3 text-sm leading-relaxed text-foreground/70">
                      {recommendation.summary}
                    </p>
                  )}

                  <div className="flex items-center justify-between border-t border-terracotta/10 pt-3">
                    <span className="text-sm font-medium text-pine">
                      {recommendation.source}
                    </span>

                    <a
                      href={recommendation.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-semibold text-terracotta hover:underline"
                    >
                      Read Original ↗
                    </a>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
