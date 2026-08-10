type Article = {
  id: string;
  title: string;
  summary: string | null;
  source: string;
  category: string;
  url: string;
  published_date: string;
};

type ArticleCardProps = {
  article: Article;
};

export default function ArticleCard({ article }: ArticleCardProps) {
  return (
    <article className="group flex h-full flex-col rounded-xl md:rounded-2xl border border-terracotta/15 bg-card p-4 md:p-5 transition-all duration-300 hover:shadow-lg hover:shadow-terracotta/5 hover:-translate-y-0.5">
      <div className="flex items-center gap-2 mb-2 md:mb-3">
        <span className="inline-flex items-center rounded-full bg-terracotta/10 px-2 py-0.5 md:px-2.5 md:py-0.5 text-xs font-medium uppercase tracking-wider text-terracotta">
          {article.category}
        </span>
        <span className="text-xs text-muted ml-auto">
          {new Date(article.published_date).toLocaleDateString()}
        </span>
      </div>

      <h2 className="text-base md:text-lg font-bold text-foreground leading-tight mb-2 line-clamp-2 group-hover:text-terracotta transition-colors">
        {article.title}
      </h2>

      {article.summary && (
        <p className="text-xs md:text-sm text-foreground/70 leading-relaxed mb-3 md:mb-4 line-clamp-3 flex-1">
          {article.summary}
        </p>
      )}

      <div className="pt-2 md:pt-3 border-t border-terracotta/10">
        <div className="flex items-center justify-between">
          <span className="text-xs md:text-sm font-medium text-pine">{article.source}</span>
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs md:text-sm font-semibold text-terracotta transition-all hover:gap-1.5"
          >
            Read
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="h-3 md:h-3.5 w-3 md:w-3.5"
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
      </div>
    </article>
  );
}
