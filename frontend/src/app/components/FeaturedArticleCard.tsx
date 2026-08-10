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
    <article className="group flex h-full flex-col rounded-2xl md:rounded-3xl border border-terracotta/20 bg-card p-4 md:p-6 transition-all duration-300 hover:shadow-xl hover:shadow-terracotta/10 hover:-translate-y-1">
      <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3 mb-3 md:mb-4">
        <span className="inline-flex items-center rounded-full bg-terracotta/15 px-2.5 md:px-3 py-0.5 md:py-1 text-xs font-semibold uppercase tracking-wider text-terracotta w-fit">
          Featured
        </span>
        <span className="inline-flex items-center rounded-full bg-pine/15 px-2.5 md:px-3 py-0.5 md:py-1 text-xs font-medium uppercase tracking-wider text-pine w-fit">
          {article.category}
        </span>
        <span className="text-xs text-muted sm:ml-auto">
          {new Date(article.published_date).toLocaleDateString()}
        </span>
      </div>

      <h2 className="text-lg md:text-2xl font-bold text-foreground leading-tight mb-2 md:mb-3 group-hover:text-terracotta transition-colors">
        {article.title}
      </h2>

      {article.summary && (
        <p className="text-sm md:text-base text-foreground/80 leading-relaxed mb-3 md:mb-4 flex-1">
          {article.summary}
        </p>
      )}

      <div className="flex items-center justify-between pt-3 md:pt-4 border-t border-terracotta/10">
        <span className="text-xs md:text-sm font-medium text-pine">{article.source}</span>
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-xs md:text-sm font-semibold text-terracotta transition-all hover:gap-1.5"
        >
          Read article
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="h-3.5 md:h-4 w-3.5 md:w-4"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M10 6H6a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2v-4M14 10l8 8"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M22 14l-8-8-4 4"
            />
          </svg>
        </a>
      </div>
    </article>
  );
}
