const API_BASE_URL = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");

export async function apiRequest(path, options = {}) {
  const token = localStorage.getItem("access_token");
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(data.message || "The API request failed");
    error.status = response.status;
    throw error;
  }

  return data;
}

export function checkApiHealth() {
  return apiRequest("/health");
}

export function login(credentials) {
  return apiRequest("/user/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

export function getProfile() {
  return apiRequest("/profile");
}

export function register(user) {
  return apiRequest("/user/register", {
    method: "POST",
    body: JSON.stringify(user),
  });
}