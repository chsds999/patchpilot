import { useState } from "react";
import ReviewForm from "./components/ReviewForm";
import ReviewResult from "./components/ReviewResult";
import { ReviewResponse } from "./api";

export default function App() {
  const [result, setResult] = useState<ReviewResponse | null>(null);

  return (
    <div className="container">
      <h1>PatchPilot</h1>
      <p className="subtitle">
        Paste code → get an AI-powered review with fixes and Before/After refactors.
      </p>

      <div className="grid">
        <div className="card">
          <ReviewForm onResult={setResult} />
        </div>
        <div className="card">
          <ReviewResult result={result} />
        </div>
      </div>
    </div>
  );
}
