
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
paste the last line of: docker compose logs migrate   (first up, then after down + up)
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

## D06 · Collecting the corpus

- Start target: Instructions + FAQs + annexures
- Collected today: ___ files, ___ pages, ___ MB (from DATASET.md)
- Doors used: URL list / Git repository / sitemap / by hand (keep the ones I used)

### Licence check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| | | |

### robots.txt

- Site: ________ . Its robots.txt says (2 lines): ________
- Was anything blocked for my bot? What did I do about it?

### Kill and resume

- Run 1: I pressed Ctrl+C after ___ files
- Run 2: downloaded=___ skipped=___
- Run 3: downloaded=0 skipped=___

### Capacity (from docs/CAPACITY.md)

- Tokens per page, measured: ___
- Full corpus: ___ M tokens, ___ chunks, embedding about Rs ___, vectors ___ MB
- The number that surprised me most, and why (2 lines):

### One thing that went wrong today, and how I fixed it
