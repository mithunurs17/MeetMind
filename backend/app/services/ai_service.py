import os
import time
import json
from typing import Any, Dict, Optional

import openai

from app.utils.nlp import preprocess_transcript, parse_date

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


DEFAULT_PROMPT = (
    "You are an assistant that extracts structured meeting minutes from a raw meeting transcript.\n"
    "Return ONLY valid JSON with the following keys:\n"
    "summary: string, decisions: [string], action_items: [{task:string, owner:string|null, due_date:string|null, status:string}], risks: [string], open_questions: [string]"  # noqa: E501
)


def call_openai_with_retries(prompt: str, max_retries: int = 3, backoff: float = 1.0) -> Optional[str]:
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = openai.ChatCompletion.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": DEFAULT_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=1000,
            )
            content = resp.choices[0].message.content
            return content
        except Exception as e:
            last_exc = e
            time.sleep(backoff * attempt)
    raise last_exc


def extract_structured_meeting(raw_text: str, title: Optional[str] = None) -> Dict[str, Any]:
    """Run preprocessing, call the LLM, validate JSON, and return structured data."""
    pre = preprocess_transcript(raw_text)

    prompt = (
        f"Transcript:\n{raw_text}\n\n"
        f"Entities detected: {json.dumps(pre.get('entities', {}))}\n\n"
        "Provide the structured JSON output as described. Dates should be ISO-8601 when possible."
    )

    raw_response = call_openai_with_retries(prompt)

    # Ensure we return valid JSON, attempt simple repairs if necessary
    for attempt in range(2):
        try:
            data = json.loads(raw_response)
            break
        except Exception:
            # Try to find the first JSON object in the text
            start = raw_response.find("{")
            end = raw_response.rfind("}")
            if start != -1 and end != -1:
                try:
                    data = json.loads(raw_response[start:end+1])
                    break
                except Exception:
                    pass
            # fallback: ask the model again more strictly
            raw_response = call_openai_with_retries(
                "The previous response was not valid JSON. Return ONLY valid JSON object with the specified keys.")
    else:
        raise ValueError("AI did not return valid JSON")

    # Post-process dates and owners
    # Normalize action item due_dates
    items = data.get("action_items", []) or []
    for it in items:
        if isinstance(it.get("due_date"), str) and it.get("due_date"):
            parsed = parse_date(it.get("due_date"))
            it["due_date"] = parsed.isoformat() if parsed else None

    # Merge NER person suggestions if owner missing
    persons = pre.get("persons", [])
    for it in items:
        if not it.get("owner") and persons:
            it["owner"] = persons[0]

    # Guarantee fields
    return {
        "title": title or "",
        "raw_text": raw_text,
        "summary": data.get("summary") or "",
        "decisions": data.get("decisions", []),
        "action_items": items,
        "risks": data.get("risks", []),
        "open_questions": data.get("open_questions", []),
    }
