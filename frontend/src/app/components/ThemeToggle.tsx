"use client";

import { FiMoon, FiSun } from "react-icons/fi";
import { useTheme } from "next-themes";

export default function ThemeToggle() {
  const { setTheme } = useTheme();

  const toggleTheme = () => {
    const isDark = document.documentElement.classList.contains("dark");

    setTheme(isDark ? "light" : "dark");
  };

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label="Toggle theme"
      className="
        flex h-9 w-9 items-center justify-center rounded-xl
        bg-gray-100 dark:bg-gray-800
      "
    >
      {/* Light mode icon */}
      <FiMoon className="block h-5 w-5 dark:hidden" />

      {/* Dark mode icon */}
      <FiSun className="hidden h-5 w-5 dark:block" />

      <span className="sr-only">Toggle theme</span>
    </button>
  );
}
