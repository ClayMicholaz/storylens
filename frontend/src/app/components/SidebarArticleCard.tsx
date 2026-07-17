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

export default function SidebarArticleCard({ article }: SidebarArticleCardProps) {
  return (
    <article className="group flex flex-col rounded-2xl border border-pine/20 bg-card p-4 transition-all duration-300 hover:shadow-lg hover:shadow-pine/10 hover:-translate-y-0.5">
      <div className="flex items-center gap-2 mb-2">
        <span className="inline-flex items-center rounded-full bg-pine/10 px-2.5 py-0.5 text-xs font-medium uppercase tracking-wider text-pine">
          {article.category}
        </span>
      </div>

      <h3 className="text-base font-semibold text-foreground leading-tight mb-2 line-clamp-2 group-hover:text-pine transition-colors">
        {article.title}
      </h3>

      <div className="mt-auto flex items-center justify-between pt-3 border-t border-pine/10">
        <span className="text-xs text-muted">{article.source}</span>
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