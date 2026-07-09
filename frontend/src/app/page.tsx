import { API_BASE_URL } from "@/lib/config";

type Article = {
  id: string;
  title: string;
  summary: string | null;
  source: string;
  category: string;
  url: string;
  published_date: string;
};

type ArticlesResponse = {
  data: Article[];
  pagination: {
    next_cursor: string | null;
    has_more: boolean;
    limit: number;
  };
};

async function getArticles(cursor?: string): Promise<ArticlesResponse> {
  const params = new URLSearchParams({ limit: "20" });
  if (cursor) params.set("cursor", cursor);

  const res = await fetch(`${API_BASE_URL}/api/articles?${params}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.error?.message ?? "Failed to fetch articles");
  }

  return res.json();
}

export default async function HomePage() {
  const { data: articles } = await getArticles();

  return (
    <main className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">StoryLens</h1>

      <div className="space-y-6">
        {articles.map((article) => (
          <article key={article.id} className="border rounded-lg p-4">
            <h2 className="text-xl font-semibold">{article.title}</h2>

            <p className="text-sm text-gray-500 mt-1">
              {article.source} • {article.category}
            </p>

            {article.summary && <p className="mt-3">{article.summary}</p>}

            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-4 underline"
            >
              Read Original Article
            </a>
          </article>
        ))}
      </div>
    </main>
  );
}