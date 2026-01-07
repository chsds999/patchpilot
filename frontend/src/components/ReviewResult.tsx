import { marked } from "marked";
import { ReviewResponse } from "../api";

type Props = {
  result: ReviewResponse | null;
};

export default function ReviewResult({ result }: Props) {
  if (!result) {
    return <p className="muted">Review output will appear here.</p>;
  }

  return (
    <>
      <p className="meta">
        Model: {result.meta.model} · Language: {result.meta.language}
      </p>
      <div
        className="markdown"
        dangerouslySetInnerHTML={{
          __html: marked.parse(result.review_markdown)
        }}
      />
    </>
  );
}
