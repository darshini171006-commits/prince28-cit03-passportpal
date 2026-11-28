
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

### Docker Compose

```text
paste the output of: docker compose ps
```

### Tests

```text
paste the output of: uv run poe cov
```

- Test result: ___
- Coverage: ___%

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
