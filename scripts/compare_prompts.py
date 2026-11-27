"""Compare PassportPal classification prompt versions.

Run:
    uv run python scripts/compare_prompts.py
"""

import asyncio
import json
from pathlib import Path

from passportpal.config import get_settings
from passportpal.llm.gateway import LLMGateway, LLMUnavailable, OpenAICompatProvider

ROOT = Path(__file__).resolve().parents[1]
PROMPT_DIR = ROOT / "prompts"
TESTSET = ROOT / "eval" / "prompt_testset.jsonl"
CACHE_FILE = ROOT / "eval" / ".prompt_cache.json"

VERSIONS = ["classify_v1.md", "classify_v2.md", "classify_v3.md"]


def load_testset() -> list[dict]:
    with TESTSET.open(encoding="utf-8") as file:
        rows = [json.loads(line) for line in file if line.strip()]

    if len(rows) != 20:
        raise ValueError(f"Expected exactly 20 test questions, found {len(rows)}")

    return rows


def load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}

    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def build_gateway() -> tuple[LLMGateway, list]:
    settings = get_settings()
    providers = []

    if settings.gemini_api_key:
        providers.append(
            OpenAICompatProvider(
                name="gemini",
                base_url=settings.llm_primary_base_url,
                api_key=settings.gemini_api_key,
                model=settings.llm_primary_model,
                timeout=settings.llm_timeout_seconds,
            )
        )

    if settings.groq_api_key:
        providers.append(
            OpenAICompatProvider(
                name="groq",
                base_url=settings.llm_fallback_base_url,
                api_key=settings.groq_api_key,
                model=settings.llm_fallback_model,
                timeout=settings.llm_timeout_seconds,
            )
        )

    if not providers:
        raise RuntimeError(
            "No LLM provider configured. Set GEMINI_API_KEY or GROQ_API_KEY in .env."
        )

    return LLMGateway(providers, usd_inr=settings.usd_inr), providers


def extract_case_type(response: str) -> str:
    """Read case_type from the model's JSON response."""
    text = response.strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3].strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return "invalid"

    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return "invalid"

    value = data.get("case_type")
    allowed = {
        "new_passport",
        "renewal",
        "lost_or_damaged",
        "minor_passport",
        "other",
    }
    return value if value in allowed else "invalid"


async def main() -> int:
    rows = load_testset()
    cache = load_cache()
    gateway, providers = build_gateway()

    try:
        for version in VERSIONS:
            prompt_path = PROMPT_DIR / version
            system_prompt = prompt_path.read_text(encoding="utf-8")
            correct = 0

            print(f"\nEvaluating {version}")

            for row in rows:
                cache_key = f"{version}:{row['id']}"

                if cache_key in cache:
                    predicted = cache[cache_key]
                else:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": row["question"]},
                    ]

                    try:
                        result = await gateway.generate(
                            messages,
                            purpose="prompt_evaluation",
                            prompt_version=version.removesuffix(".md"),
                            temperature=0,
                        )
                    except LLMUnavailable as exc:
                        print(f"\nStopped: no model can answer ({exc})")
                        print("Wait and run the same command again; completed answers are cached.")
                        return 1

                    predicted = extract_case_type(result.text)
                    cache[cache_key] = predicted
                    save_cache(cache)

                expected = row["expected"]
                if predicted == expected:
                    correct += 1

                print(
                    f"{row['id']}: expected={expected}, "
                    f"predicted={predicted}, "
                    f"{'PASS' if predicted == expected else 'FAIL'}"
                )

            accuracy = correct / len(rows) * 100
            print(f"{version}: {correct}/{len(rows)} correct ({accuracy:.1f}%)")

    finally:
        for provider in providers:
            await provider._client.aclose()

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
