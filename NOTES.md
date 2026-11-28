
# PassportPal — Development Notes

## D04 · Docker, Compose and tests

### The image

```text
paste the output of: docker images passportpal:dev
paste the output of: docker run --rm passportpal:dev id
```

- Size: ___ MB (target: under 400 MB)
- First build: ___ s. After changing one line of code: ___ s.
- Which step said CACHED, and why? (1 line, your own words)

### The stack

```text
paste the output of: docker compose ps -a
paste the last line of: docker compose logs migrate (first up, then after down + up)
```

### Breaking the database on purpose

```text
db stopped:  /health → paste
db stopped:  /ready  → paste
db started:  /ready  → paste
```

Why should a load balancer stop sending traffic here but not restart the app? (2 lines)

### Tests and coverage

```text
uv run poe test              → paste the last line
uv run poe test-integration  → paste the last line
coverage TOTAL, unit only    → paste
coverage TOTAL, with integration tests → paste
```

Two files or lines my coverage report says are never run, and whether they matter: (2 lines)

---

## D05 · CI/CD and going live

### CI

- Workflow: `.github/workflows/ci.yml`
- CI checks: formatting, linting, type checking and tests.

### CD

- Workflow: `.github/workflows/cd.yml`
- Deployment configuration and health checks are included.

### Deployment

- Application health endpoint: `/health`
- Readiness endpoint: `/ready`

---

## D06 · Collecting the corpus

### Dataset

- Dataset documentation: `DATASET.md`
- Source list: `data/sources.csv`
- Manifest: `data/manifest.jsonl`
- Raw documents: `data/raw/`

### Fetching

- Script: `scripts/fetch.py`
- Parser script: `scripts/parse_corpus.py`
- Dataset report: `scripts/dataset_report.py`

### Validation

- Documents are collected from their source URLs.
- SHA-256 hashes are used to identify document content.
- The manifest records collected documents.

---

## D07 · Parser comparison

### Parser implementations

- PyMuPDF
- pypdf

### Comparison

- Script: `scripts/compare_parsers.py`
- Compare extracted text, page count and heading quality.

### Dataset parsing

- Script: `scripts/parse_corpus.py`
- Parsed documents are stored in the database.

---

## D08 · LLM gateway

### Implementation

- LLM gateway: `src/passportpal/llm/gateway.py`
- Chat endpoint: `src/passportpal/api/routes/chat.py`
- LLM call tracking: `src/passportpal/db/llm_calls.py`
- System prompt: `prompts/chat_system_v1.md`

### Features

- LLM provider abstraction.
- Fallback provider support.
- Streaming chat responses.
- LLM call tracking.
- Token usage and latency tracking.
- Error and fallback tracking.

### API

- Chat endpoint: `/v1/chat`
- Health endpoint: `/health`
- Readiness endpoint: `/ready`

### Tests

- Gateway unit tests: `tests/unit/test_gateway.py`
- Chat API tests: `tests/unit/test_chat_api.py`
- LLM tracking tests: `tests/integration/test_llm_calls.py`

### LLM ping

```powershell
uv run python scripts/llm_ping.py
```

### Provider configuration and performance

- Primary: gemini-3.8-flash (Gemini)
- Fallback: openai/gpt-oss-20b (Groq)
- First question on my laptop: first words after ___ s, total ___ s, tokens in ___ / out ___, cost Rs ___
- Same question on my live URL (second, awake request): first words after ___ s. Day 1 target: under 1.5 s

### Tokens: English against Tamil

| Message | tokens in |
|---|---|
| "Hi" (baseline: mostly my system prompt) | |
| The English sentence | |
| The same sentence in Tamil | |

- The Tamil message needs about ___ times the tokens of the English one.

### What the model does without my documents

- Question 6 ("When will my police verification be done?"): did it admit it can't know? Its exact words:
- A detail it got wrong or invented (question → what it said → what is true):
- The off-topic question: did it decline in one sentence?

### Fallback and circuit breaker

- With the primary broken: provider ________, fallback ________, first words after ___ s
- The question at which "llm call gemini ... error" stopped appearing in the log: number ___

### The bill

- `/v1/usage` today: calls ___, errors ___, fallbacks ___, cost Rs ___
- Average per answered question: Rs ___ (my Day 1 target: under Rs 0.50)

### One thing that went wrong today, and how I fixed it

---

## D09 · Prompt engineering and structured extraction

### Prompt evaluation

Test dataset: `eval/prompt_testset.jsonl`

- Number of test cases: 20
- Evaluation command: `uv run python scripts/compare_prompts.py`

| Prompt version | Correct | Accuracy |
|---|---:|---:|
| classify_v1.md | 20/20 | 100% |
| classify_v2.md | 20/20 | 100% |
| classify_v3.md | 20/20 | 100% |

### Structured passport extraction

- Prompt: `prompts/extract_v1.md`
- Implementation: `src/passportpal/llm/extract.py`
- Function: `extract_fields()`
- Output fields:
  - `case_type`
  - `document`
  - `annexure`
  - `fee`
  - `condition`

- Missing or unknown values are returned as `None`.
- Empty input and invalid JSON are rejected.
- LLM calls use the gateway with purpose `passport_extraction` and prompt version `extract_v1`.

### Extraction unit tests

Command:

```powershell
uv run pytest -q tests/unit/test_extract.py
```

Result: 5 passed.

### Overall non-integration tests

Command:

```powershell
uv run pytest -q --ignore=tests/integration
```

Result: 41 passed.

### Integration tests

Command:

```powershell
uv run pytest -q
```

Result: 36 passed, 4 setup errors.

Reason: `TEST_DATABASE_URL` is not configured for the PostgreSQL integration tests.

Status: Integration tests still need verification with a configured test database.
