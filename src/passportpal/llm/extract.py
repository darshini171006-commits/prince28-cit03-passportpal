"""Extract structured passport information using the LLM gateway."""

import json
from pathlib import Path
from typing import Any

from passportpal.llm.gateway import LLMGateway

PROMPT_PATH = Path("prompts/extract_v1.md")

FIELDS = ("case_type", "document", "annexure", "fee", "condition")


def _parse_json(response: str) -> dict[str, Any]:
    """Parse a JSON object from an LLM response."""
    text = response.strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3].strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("The LLM response does not contain a JSON object.")

    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError("The LLM returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise ValueError("The LLM response must be a JSON object.")

    return data


async def extract_fields(
    text: str,
    gateway: LLMGateway,
    *,
    prompt_path: Path = PROMPT_PATH,
) -> dict[str, Any]:
    """Extract case_type, document, annexure, fee, and condition."""
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    system_prompt = prompt_path.read_text(encoding="utf-8")

    result = await gateway.generate(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text.strip()},
        ],
        purpose="passport_extraction",
        prompt_version="extract_v1",
        temperature=0,
    )

    extracted = _parse_json(result.text)

    # Always return the same five keys, even if the model omits a field.
    return {
        field: extracted.get(field)
        if extracted.get(field) not in ("", "unknown", "Unknown")
        else None
        for field in FIELDS
    }


# Alternative descriptive name for callers.
extract_passport_info = extract_fields
