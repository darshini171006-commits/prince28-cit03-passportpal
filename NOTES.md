
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
