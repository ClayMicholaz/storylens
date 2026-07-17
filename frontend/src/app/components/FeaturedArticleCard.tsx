type Article = {
  id: string;
  title: string;
  summary: string | null;
  source: string;
  category: string;
  url: string;
  published_date: string;
};

type FeaturedArticleCardProps = {
  article: Article;
};

export default function FeaturedArticleCard({ article }: FeaturedArticleCardProps) {
  return (
    <article className="group flex h-full flex-col rounded-3xl border border-terracotta/20 bg-white p-6 transition-all duration-300 hover:shadow-xl hover:shadow-terracotta/10 hover:-translate-y-1">
      <div className="flex items-center gap-2 mb-4">
        <span className="inline-flex items-center rounded-full bg-terracotta/15 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-terracotta">
          Featured
        </span>
        <span className="inline-flex items-center rounded-full bg-pine/15 px-3 py-1 text-xs font-medium uppercase tracking-wider text-pine">
          {article.category}
        </span>
        <span className="text-xs text-muted ml-auto">
          {new Date(article.published_date).toLocaleDateString()}
        </span>
      </div>

      <h2 className="text-2xl font-bold text-[#2D3748] leading-tight mb-3 group-hover:text-terracotta transition-colors">
        {article.title}
      </h2>

      {article.summary && (
        <p className="text-base text-[#2D3748]/80 leading-relaxed mb-4 flex-1">
          {article.summary}
        </p>
      )}

      <div className="flex items-center justify-between pt-4 border-t border-terracotta/10">
        <span className="text-sm font-medium text-pine">{article.source}</span>
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-terracotta transition-all hover:gap-2"
        >
          Read article
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="h-4 w-4"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M4.5 19.5l15-15M19.5 4.5v15M4.5 9.5h15"
            />
          </svg>
        </a>
      </div>
    </article>
  );
}