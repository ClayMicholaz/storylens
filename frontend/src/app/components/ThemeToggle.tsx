"use client";

import { useSyncExternalStore } from "react";
import { useTheme } from "next-themes";
import { FiMoon, FiSun } from "react-icons/fi";

const emptySubscribe = () => () => {};

function useMounted() {
  return useSyncExternalStore(
    emptySubscribe,
    () => true, // client snapshot: we're mounted
    () => false, // server snapshot: not mounted yet
  );
}

export default function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const mounted = useMounted();

  const isDark = resolvedTheme === "dark";

  const toggleTheme = () => {
    setTheme(isDark ? "light" : "dark");
  };

    if (!mounted) {
      return (
        <button
          type="button"
          aria-label="Toggle theme"
          className="flex h-9 w-9 items-center justify-center rounded-xl bg-terracotta/10 text-terracotta cursor-pointer"
        >
          <span className="sr-only">Toggle theme</span>
          <FiMoon className="h-5 w-5" />
        </button>
      );
    }

    return (
      <button
        type="button"
        aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
        onClick={toggleTheme}
        className={`
        flex h-9 w-9 items-center justify-center rounded-xl
        bg-terracotta/10 text-terracotta transition-colors cursor-pointer
        hover:bg-terracotta/20
        dark:bg-pine/10 dark:text-pine dark:hover:bg-pine/20
      `}
      >
        <span className="sr-only">Toggle theme</span>
        {isDark ? (
          <FiSun className="h-5 w-5" />
        ) : (
          <FiMoon className="h-5 w-5" />
        )}
      </button>
    );
}
