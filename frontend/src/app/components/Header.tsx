"use client";

type HeaderProps = {
  searchQuery?: string;
  onSearchChange?: (value: string) => void;
};

export default function Header({ searchQuery = "", onSearchChange }: HeaderProps) {
  return (
    <header className="sticky top-0 z-10 bg-[#FEFCF7]/80 backdrop-blur-sm border-b border-[#E07A5F]/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 md:py-4">
        {/* Mobile Layout: Stacked vertically */}
        <div className="flex flex-col md:hidden gap-3">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-2xl bg-linear-to-tr from-[#E07A5F] to-[#3D7A65] flex items-center justify-center shadow-md shadow-[#E07A5F]/20">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                  stroke="currentColor"
                  className="h-4 w-4 text-white"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 6.042A8 8 0 7018 14.042V16.5A2.5 2.5 0 0115.5 19h-3A2.5 2.5 0 0110 16.5V14.042A8 8 0 0012 6.042z"
                  />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-[#2D3748]">StoryLens</h1>
            </div>
            <a 
              href="/auth/login" 
              className="rounded-xl bg-[#E07A5F]/10 px-3 py-1.5 text-sm font-semibold text-[#E07A5F] transition-colors hover:bg-[#E07A5F]/20"
            >
              Sign in
            </a>
          </div>
          
          {/* Mobile Search - Full width */}
          <div className="relative">
            <input
              type="search"
              placeholder="Search articles..."
              value={searchQuery}
              onChange={(e) => onSearchChange?.(e.target.value)}
              className="w-full rounded-xl border border-[#E07A5F]/20 bg-white px-4 py-2.5 pl-10 text-sm text-[#2D3748] placeholder-[#8D99AE] outline-none transition-all duration-200 focus:border-[#E07A5F] focus:ring-4 focus:ring-[#E07A5F]/10"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#8D99AE]"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M21 21l-5.5-5.5m2.5-5.5a7.5 7.5 0 11-15 0 7.5 7.5 0 0115 0z"
              />
            </svg>
          </div>
        </div>

        {/* Desktop/Tablet Layout: Logo left, centered search, auth right */}
        <div className="hidden md:flex relative items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-2xl bg-linear-to-tr from-[#E07A5F] to-[#3D7A65] flex items-center justify-center shadow-md shadow-[#E07A5F]/20">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="h-5 w-5 text-white"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 6.042A8 8 0 7018 14.042V16.5A2.5 2.5 0 0115.5 19h-3A2.5 2.5 0 0110 16.5V14.042A8 8 0 0012 6.042z"
                />
              </svg>
            </div>
            <div className="flex flex-col">
              <h1 className="text-2xl font-bold text-[#2D3748]">StoryLens</h1>
              <p className="text-[#8D99AE] text-sm font-medium">Cut through the noise. Read what matters.</p>
            </div>
          </div>

          {/* Auth Links */}
          <a 
            href="/auth/login" 
            className="rounded-xl bg-[#E07A5F]/10 px-4 py-2 text-sm font-semibold text-[#E07A5F] transition-colors hover:bg-[#E07A5F]/20"
          >
            Sign in
          </a>

          {/* Centered Search */}
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md">
            <div className="relative">
              <input
                type="search"
                placeholder="Search articles..."
                value={searchQuery}
                onChange={(e) => onSearchChange?.(e.target.value)}
                className="w-full rounded-xl border border-[#E07A5F]/20 bg-white px-4 py-2.5 pl-10 text-sm text-[#2D3748] placeholder-[#8D99AE] outline-none transition-all duration-200 focus:border-[#E07A5F] focus:ring-4 focus:ring-[#E07A5F]/10"
              />
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#8D99AE]"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M21 21l-5.5-5.5m2.5-5.5a7.5 7.5 0 11-15 0 7.5 7.5 0 0115 0z"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
