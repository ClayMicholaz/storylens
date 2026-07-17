"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { API_BASE_URL } from "@/lib/config";

type AuthResponse = {
  access_token: string;
  refresh_token: string;
};

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const body = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(body?.error?.message ?? body?.detail ?? "Registration failed");
      }

      const data = body as AuthResponse;
      localStorage.setItem("storylens_access_token", data.access_token);
      localStorage.setItem("storylens_refresh_token", data.refresh_token);
      router.push("/");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="relative flex min-h-[85vh] flex-col items-center justify-center px-4 py-16 sm:px-6 lg:px-8">
      {/* Decorative background glows */}
      <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-[40%] -left-[20%] h-[80%] w-[80%] rounded-full bg-terracotta/10 blur-[120px]" />
        <div className="absolute -bottom-[40%] -right-[20%] h-[80%] w-[80%] rounded-full bg-pine/10 blur-[120px]" />
      </div>

      <div className="w-full max-w-md transform transition-all duration-300">
        <div className="rounded-3xl border border-pine/20 bg-card p-8 shadow-xl shadow-pine/10 sm:p-10">
          
          {/* Logo Icon & Header */}
          <div className="flex flex-col items-center text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-tr from-terracotta to-pine text-white shadow-lg shadow-terracotta/20">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2.5}
                stroke="currentColor"
                className="h-6 w-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.251 0-4.37-.59-6.224-1.625z"
                />
              </svg>
            </div>
            <h1 className="mt-6 text-3xl font-bold tracking-tight text-foreground">
              Create account
            </h1>
            <p className="mt-2 text-sm text-muted">
              Register your StoryLens account to get started.
            </p>
          </div>

          {/* Form */}
          <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted">
                Email Address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="mt-2 w-full rounded-xl border border-pine/20 bg-pine/5 px-4 py-3 text-sm text-foreground placeholder-muted outline-none transition-all duration-200 focus:border-pine focus:bg-card focus:ring-4 focus:ring-pine/10"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted">
                Password
              </label>
              <input
                type="password"
                required
                minLength={8}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-2 w-full rounded-xl border border-pine/20 bg-pine/5 px-4 py-3 text-sm text-foreground placeholder-muted outline-none transition-all duration-200 focus:border-pine focus:bg-card focus:ring-4 focus:ring-pine/10"
                placeholder="At least 8 characters"
              />
            </div>

            {error && (
              <div className="rounded-xl border border-terracotta/30 bg-terracotta/10 p-3.5 text-sm text-terracotta">
                <div className="flex gap-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    className="h-5 w-5 shrink-0 text-terracotta"
                  >
                    <path
                      fillRule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <span>{error}</span>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-terracotta to-pine py-3.5 px-4 text-sm font-semibold text-white shadow-md shadow-terracotta/20 transition-all duration-200 hover:from-terracotta/90 hover:to-pine/90 hover:shadow-lg hover:shadow-terracotta/30 active:scale-[0.98] disabled:pointer-events-none disabled:opacity-60"
            >
              {isSubmitting ? (
                <>
                  <svg
                    className="h-4 w-4 animate-spin text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  <span>Creating account...</span>
                </>
              ) : (
                "Create Account"
              )}
            </button>
          </form>

          {/* Switch Link */}
          <div className="mt-8 text-center text-sm text-muted">
            Already have an account?{" "}
            <Link
              href="/auth/login"
              className="font-semibold text-terracotta hover:text-terracotta/80 transition-colors"
            >
              Sign in
            </Link>
          </div>

        </div>
      </div>
    </main>
  );
}