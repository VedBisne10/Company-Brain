const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, { headers: { "Content-Type": "application/json" }, ...options });
  if (!response.ok) throw new Error((await response.text()) || "Request failed");
  return response.json();
}

export function askQuestion(question) {
  return request("/chat", { method: "POST", body: JSON.stringify({ question }) });
}

export function searchKnowledge(query) {
  return request(`/search?q=${encodeURIComponent(query)}`);
}
