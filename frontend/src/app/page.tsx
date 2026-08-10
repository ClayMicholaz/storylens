import { API_BASE_URL } from "@/lib/config";
import Header from "./components/Header";
import FeaturedArticleCard from "./components/FeaturedArticleCard";
import SidebarArticleCard from "./components/SidebarArticleCard";
import ArticleCard from "./components/ArticleCard";
import EmptyState from "./components/EmptyState";

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

async function getArticles(): Promise<ArticlesResponse> {
  const res = await fetch(`${API_BASE_URL}/api/articles?limit=20`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch articles");
  }

  return res.json();
}

export default async function HomePage() {
  let articles: Article[] = [];
  let loadError: string | null = null;

  try {
    const response = await getArticles();
    articles = response.data;
  } catch (error) {
    loadError = error instanceof Error ? error.message : "Failed to load articles";
  }

  // Get first article for featured card, next 3 for sidebar, rest for grid
  const featuredArticle = articles[0];
  const sidebarArticles = articles.slice(1, 4);
  const gridArticles = articles.slice(4);

  return (
    <>
      <Header />

      <main className="flex-1 bg-background min-h-[calc(100vh-64px)] md:min-h-[calc(100vh-72px)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-12">

          {loadError && (
            <div className="mb-6 md:mb-8 rounded-2xl border border-terracotta/30 bg-terracotta/5 p-4 md:p-6 text-terracotta">
              <p className="font-semibold mb-1">Articles are temporarily unavailable.</p>
              <p className="text-sm">{loadError}</p>
            </div>
          )}

          {!loadError && articles.length === 0 && (
            <EmptyState />
          )}

          {!loadError && articles.length > 0 && (
            <>
              {/* Featured + Sidebar Section */}
              <div className="mb-8 md:mb-12 flex flex-col lg:flex-row gap-4 md:gap-6">
                {/* Featured Article */}
                <div className="flex-1">
                  <FeaturedArticleCard article={featuredArticle} />
                </div>

                {/* Sidebar Articles */}
                <div className="flex flex-col gap-3 md:gap-4 lg:w-[35%]">
                  {sidebarArticles.map((article) => (
                    <SidebarArticleCard key={article.id} article={article} />
                  ))}
                </div>
              </div>

              {/* More Articles Grid */}
              {gridArticles.length > 0 && (
                <div>
                  <h2 className="mb-4 md:mb-6 text-lg font-bold text-foreground">
                    More Stories
                  </h2>
                  <div className="grid gap-4 md:gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {gridArticles.map((article) => (
                      <ArticleCard key={article.id} article={article} />
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </>
  );
}
