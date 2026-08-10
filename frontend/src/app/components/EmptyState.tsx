type EmptyStateProps = {
  title?: string;
  description?: string;
};

export default function EmptyState({
  title = "No articles yet",
  description = "Check back later for fresh stories.",
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 md:py-16 px-4 text-center">
      <div className="mb-4 md:mb-6 flex h-16 md:h-20 w-16 md:w-20 items-center justify-center rounded-2xl md:rounded-3xl bg-terracotta/10">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="h-8 md:h-10 w-8 md:w-10 text-terracotta"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 6.042A8 8 0 7018 14.042V16.5A2.5 2.5 0 0115.5 19h-3A2.5 2.5 0 0110 16.5V14.042A8 8 0 0012 6.042z"
          />
        </svg>
      </div>
      <h3 className="text-lg md:text-xl font-bold text-foreground mb-1.5 md:mb-2">{title}</h3>
      <p className="text-sm text-muted max-w-sm">{description}</p>
    </div>
  );
}
