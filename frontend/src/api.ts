const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export type ReviewRequest = {
  language: string;
  code: string;
  goals: string[];
  context?: string;
  strictness: "gentle" | "balanced" | "strict";
};

export type ReviewResponse = {
  review_markdown: string;
  meta: Record<string, any>;
};

export async function submitReview(
  payload: ReviewRequest
): Promise<ReviewResponse> {
  const res = await fetch(`${API_BASE}/api/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Request failed");
  }

  return res.json();
}
