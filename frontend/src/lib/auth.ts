"use client";
import { API_BASE_URL } from "./config";

export async function refreshTokens() {
  const refreshToken = localStorage.getItem("storylens_refresh_token");

  const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!response.ok) {
    localStorage.removeItem("storylens_access_token");
    localStorage.removeItem("storylens_refresh_token");
    window.location.assign("/auth/login");
    return null;
  }

  const data = await response.json();
  localStorage.setItem("storylens_access_token", data.access_token);
  localStorage.setItem("storylens_refresh_token", data.refresh_token);
  return data.access_token;
}