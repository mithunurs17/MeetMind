import os
import time
import json
import re
from typing import Any, Dict, List, Optional

import openai

from app.utils.nlp import preprocess_transcript, parse_date

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

DEFAULT_PROMPT = (
    "You are an assistant that extracts structured meeting minutes from a raw meeting transcript.\n"
    "Return ONLY valid JSON with these keys:\n"
    "summary: string, decisions: [string], action_items: [{task:string, owner:string|null, due_date:string|null, status:string}], risks: [string], open_questions: [string]\n"
    "Use ISO-8601 date formats when possible. Use null for missing owner or due_date.\n"
    "Do not include any explanation outside the JSON object."
)


def call_openai_with_retries(prompt: str, max_retries: int = 3, backoff: float = 1.0) -> str:
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
                max_tokens=1200,
            )
            return resp.choices[0].message.content
        except Exception as e:
            last_exc = e
            time.sleep(backoff * attempt)
    raise last_exc


def extract_json_object(raw_text: str) -> Dict[str, Any]:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw_text, flags=re.S)
        if match:
            return json.loads(match.group(0))
    raise ValueError("AI did not return valid JSON")


def normalize_ai_response(data: Dict[str, Any], title: str, raw_text: str, persons: List[str]) -> Dict[str, Any]:
    def ensure_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    action_items = []
    for item in ensure_list(data.get("action_items", [])):
        if not isinstance(item, dict):
            continue
        due_date = item.get("due_date")
        parsed_due = parse_date(due_date) if isinstance(due_date, str) else due_date
        owner = item.get("owner") or (persons[0] if persons else None)
        action_items.append({
            "task": str(item.get("task", "")).strip(),
            "owner": owner,
            "due_date": parsed_due.isoformat() if parsed_due else None,
            "status": str(item.get("status", "pending") or "pending").strip().lower(),
        })

    return {
        "title": title or "AI Generated Meeting",
        "raw_text": raw_text,
        "summary": str(data.get("summary") or "").strip(),
        "decisions": [str(item).strip() for item in ensure_list(data.get("decisions", [])) if str(item).strip()],
        "action_items": action_items,
        "risks": [str(item).strip() for item in ensure_list(data.get("risks", [])) if str(item).strip()],
        "open_questions": [str(item).strip() for item in ensure_list(data.get("open_questions", [])) if str(item).strip()],
    }


def build_prompt(raw_text: str, title: Optional[str], preprocessed: Dict[str, Any]) -> str:
    persons = preprocessed.get("persons", [])
    orgs = preprocessed.get("orgs", [])
    entities = preprocessed.get("entities", {})
    return (
        f"Title: {title or 'Untitled Meeting'}\n"
        f"Transcript:\n{raw_text}\n\n"
        f"Detected People: {persons}\n"
        f"Detected Organizations: {orgs}\n"
        f"Detected Entities: {json.dumps(entities)}\n\n"
        "Extract an executive summary, decisions, action items, risks, and open questions. "
        "Return ONLY valid JSON without any surrounding markdown or commentary. "
        "If a field is empty, return an empty list or an empty string as appropriate."
    )


def extract_structured_meeting(raw_text: str, title: Optional[str] = None) -> Dict[str, Any]:
    pre = preprocess_transcript(raw_text)
    prompt = build_prompt(raw_text, title, pre)
    raw_response = call_openai_with_retries(prompt)

    for attempt in range(2):
        try:
            data = extract_json_object(raw_response)
            break
        except Exception:
            raw_response = call_openai_with_retries(
                "The previous response was not valid JSON. Return ONLY a valid JSON object with summary, decisions, action_items, risks, and open_questions.")
    else:
        raise ValueError("AI did not return valid JSON")

    return normalize_ai_response(data, title, raw_text, pre.get("persons", []))
