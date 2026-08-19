import Link from "next/link";

type Article = {
  id: string;
  title: string;
  summary: string | null;
  source: string;
  category: string;
  url: string;
  published_date: string;
};

type SidebarArticleCardProps = {
  article: Article;
};

export default function SidebarArticleCard({
  article,
}: SidebarArticleCardProps) {
  return (
    <article className="group flex flex-col rounded-xl md:rounded-2xl border border-pine/20 bg-card p-3 md:p-4 transition-all duration-300 hover:shadow-lg hover:shadow-pine/10 hover:-translate-y-0.5">
      <div className="flex flex-wrap items-center gap-2 mb-2">
        {/* For You badge */}
        <span className="inline-flex items-center rounded-full bg-terracotta/15 px-2.5 md:px-3 py-0.5 md:py-1 text-xs font-semibold uppercase tracking-wider text-terracotta">
          For You
        </span>

        {/* Category */}
        <span className="inline-flex items-center rounded-full bg-pine/10 px-2 md:px-2.5 py-0.5 text-xs font-medium uppercase tracking-wider text-pine">
          {article.category}
        </span>

        <span className="ml-auto text-xs text-muted">
          {new Date(article.published_date).toLocaleDateString()}
        </span>
      </div>

      {/* Internal article link */}
      <Link href={`/articles/${article.id}`}>
        <h3 className="text-sm md:text-base font-semibold text-foreground leading-tight mb-2 line-clamp-2 group-hover:text-pine transition-colors">
          {article.title}
        </h3>
      </Link>

      {/* Footer */}
      <div className="mt-auto flex items-center justify-between pt-2 md:pt-3 border-t border-pine/10">
        <span className="text-xs text-muted">{article.source}</span>

        {/* Original article */}
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs font-semibold text-pine transition-colors hover:text-pine-light"
        >
          Read →
        </a>
      </div>
    </article>
  );
}
