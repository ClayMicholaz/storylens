"use client";

import ThemeToggle from "./ThemeToggle";

export default function Header() {
  return (
    <header className="sticky top-0 z-10 bg-background/80 backdrop-blur-sm border-b border-terracotta/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 md:py-4">
        {/* Mobile Layout: Stacked vertically */}
        <div className="flex flex-col md:hidden gap-3">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-2xl bg-linear-to-tr from-terracotta to-pine flex items-center justify-center shadow-md shadow-terracotta/20">
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
                    d="M15.75 15.75l-2.489-2.489m0 0a3.375 3.375 0 10-4.773-4.773 3.375 3.375 0 004.774 4.774zM21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-foreground">StoryLens</h1>
            </div>
            <div className="flex items-center gap-2">
              <ThemeToggle />
              <a
                href="/auth/login"
                className="rounded-xl bg-terracotta/10 px-3 py-1.5 text-sm font-semibold text-terracotta transition-colors hover:bg-terracotta/20"
              >
                Sign in
              </a>
            </div>
          </div>
        </div>

        {/* Desktop/Tablet Layout: Logo left, auth right */}
        <div className="hidden md:flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-2xl bg-linear-to-tr from-terracotta to-pine flex items-center justify-center shadow-md shadow-terracotta/20">
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
                  d="M15.75 15.75l-2.489-2.489m0 0a3.375 3.375 0 10-4.773-4.773 3.375 3.375 0 004.774 4.774zM21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">StoryLens</h1>
              <p className="text-muted text-sm font-medium">
                Cut through the noise. Read what matters.
              </p>
            </div>
          </div>

          {/* Auth Links + Theme Toggle */}
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <a
              href="/auth/login"
              className="rounded-xl bg-terracotta/10 px-4 py-2 text-sm font-semibold text-terracotta transition-colors hover:bg-terracotta/20"
            >
              Sign in
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}
