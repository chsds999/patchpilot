import { useState } from "react";
import { submitReview, ReviewResponse } from "../api";

type Props = {
  onResult: (r: ReviewResponse) => void;
};

const GOALS = [
  "correctness",
  "security",
  "performance",
  "readability",
  "maintainability",
  "testing"
];

export default function ReviewForm({ onResult }: Props) {
  const [language, setLanguage] = useState("typescript");
  const [strictness, setStrictness] =
    useState<"gentle" | "balanced" | "strict">("balanced");
  const [goals, setGoals] = useState<string[]>(["readability", "correctness"]);
  const [code, setCode] = useState("");
  const [context, setContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function toggleGoal(goal: string) {
    setGoals((prev) =>
      prev.includes(goal)
        ? prev.filter((g) => g !== goal)
        : [...prev, goal]
    );
  }

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const result = await submitReview({
        language,
        code,
        goals,
        context: context || undefined,
        strictness
      });
      onResult(result);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <label>Language</label>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="typescript">TypeScript</option>
        <option value="javascript">JavaScript</option>
        <option value="python">Python</option>
        <option value="java">Java</option>
        <option value="go">Go</option>
      </select>

      <label>Strictness</label>
      <select
        value={strictness}
        onChange={(e) => setStrictness(e.target.value as any)}
      >
        <option value="gentle">Gentle</option>
        <option value="balanced">Balanced</option>
        <option value="strict">Strict</option>
      </select>

      <label>Goals</label>
      <div className="goal-row">
        {GOALS.map((g) => (
          <button
            key={g}
            className={goals.includes(g) ? "active" : ""}
            onClick={() => toggleGoal(g)}
            type="button"
          >
            {g}
          </button>
        ))}
      </div>

      <label>Context (optional)</label>
      <input
        value={context}
        onChange={(e) => setContext(e.target.value)}
        placeholder="Production API, latency-sensitive, etc."
      />

      <label>Code</label>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Paste your code here…"
      />

      {error && <div className="error">{error}</div>}

      <button onClick={handleSubmit} disabled={loading || !code.trim()}>
        {loading ? "Reviewing..." : "Get Review"}
      </button>
    </>
  );
}
