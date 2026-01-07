import os
from typing import Dict, List, Optional, Tuple

import openai

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use ~~~ inside this string so copy/paste never breaks due to nested ``` fences.
SYSTEM_PROMPT = """You are an expert senior software engineer and code reviewer.

Your job:
- Review the user's code and produce a HIGH-SIGNAL, practical review.
- Be specific: point to concrete issues, edge cases, and improvements.
- Include security, correctness, performance, maintainability, and readability.
- Provide "Before" and "After" snippets for key improvements (at least 2).
- If something is ambiguous, state assumptions and suggest questions to ask.

Output must be valid Markdown and follow this structure:

# Summary
- 3–6 bullet points of the biggest wins.

# Correctness & Bugs
- Findings with reasoning.

# Security
- Findings with severity labels: [Low], [Med], [High]

# Performance
- Findings and alternatives.

# Readability & Maintainability
- Findings including naming, structure, duplication.

# Suggested Refactor Plan (Small → Large)
1. ...
2. ...

# Before/After Examples
## Example 1
**Before**
~~~lang
...
~~~
**After**
~~~lang
...
~~~

## Example 2
**Before**
~~~lang
...
~~~
**After**
~~~lang
...
~~~

# Tests to Add
- Bullet list with concrete test cases.

# Final Notes
- Quick wrap-up.
"""

def _clamp(text: str, limit: int) -> str:
    text = text or ""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n/* …truncated… */"

def build_user_prompt(
    language: str,
    code: str,
    goals: List[str],
    context: Optional[str],
    strictness: str,
) -> str:
    goals_str = ", ".join(goals) if goals else "readability, correctness"
    ctx = context.strip() if context else "None provided."
    return (
        f"Language: {language}\n"
        f"Strictness: {strictness}\n"
        f"Focus goals: {goals_str}\n"
        f"Context: {ctx}\n\n"
        f"Code:\n~~~{language}\n{code}\n~~~\n"
    )

def run_review(
    language: str,
    code: str,
    goals: List[str],
    context: Optional[str],
    strictness: str,
) -> Tuple[str, Dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    max_chars = int(os.getenv("MAX_CODE_CHARS", "50000"))
    safe_code = _clamp(code, max_chars)

    user_prompt = build_user_prompt(language, safe_code, goals, context, strictness)

    # Classic OpenAI Python client call (stable) — avoids OpenAI(...) client init.
    resp = openai.ChatCompletion.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    review_text = resp["choices"][0]["message"]["content"] or ""

    meta = {
        "model": DEFAULT_MODEL,
        "language": language,
        "original_chars": len(code or ""),
        "processed_chars": len(safe_code),
    }
    return review_text, meta
