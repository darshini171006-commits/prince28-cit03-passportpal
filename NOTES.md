
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

- Live URL: (paste your actual deployed PassportPal URL)
- CI run for pull request 1: (paste the actual GitHub Actions run link)
- First deploy that ran by itself: (paste the actual CD run link)
- Merge clicked at __:__ → "Smoke test passed" at __:__ → lead time: ___ min

### Smoke test output from that CD run

```text
paste the last 4 lines of the "Smoke test the live URL" step
```

### Rollback drill

- Rolled back to sha ________ : started __:__, smoke passed __:__ (___ min)
- Rolled forward to sha ________ : ___ min
- During the rollback, the database stayed on the newer schema. Why is that safe here? (2 lines)

### Where my secrets live

- Neon string: GitHub Secret DATABASE_URL + Render environment. Not in Git, not in the image.
- Render deploy hook: GitHub Secret RENDER_DEPLOY_HOOK only.

### Monitoring

- UptimeRobot checks /health every 5 minutes; alerts go to my email.
- One thing that would make my live app faster on its first request: (1 line)

---

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

---

## D07 · Parser comparison

<!-- parsers:start -->
| File | Parsers (A / B) | Pages | A found | B found | Time (A / B) | Better, why |
|---|---|---|---|---|---|---|
| passport1980-4547326d.pdf | PyMuPDF / pypdf | - | FAILED: no_text_layer | FAILED: no_text_layer | 0.23 s / 0.09 s | |
| steps-to-apply-for-passport-services-f9aff960.pd | PyMuPDF / pypdf | 29 | 2,137 chars, 16 headings, 0 tables | 2,066 chars, 0 headings, 0 tables | 2.86 s / 0.19 s | |
| steps-to-submit-an-application-at-psk-179ee910.p | PyMuPDF / pypdf | 17 | 2,952 chars, 13 headings, 0 tables | 2,898 chars, 0 headings, 0 tables | 0.19 s / 0.24 s | |
| sql-databases-5b402114.html | trafilatura / strip tags | 47 | 96,339 chars, 47 headings, 0 tables | 117,570 chars, 35 headings, 0 tables | 6.06 s / 0.14 s | |
| applicationforminstructionbooklet-v3-0-470b5b24. | PyMuPDF / pypdf | 21 | 80,545 chars, 66 headings, 20 tables | 74,733 chars, 0 headings, 0 tables | 17.63 s / 5.99 s | |
| citizen-charter-e6c529c9.pdf | PyMuPDF / pypdf | 11 | 55,313 chars, 14 headings, 10 tables | 18,260 chars, 0 headings, 0 tables | 8.82 s / 1.59 s | |
| oauth2-jwt-657ba832.html | trafilatura / strip tags | 19 | 40,295 chars, 19 headings, 0 tables | 50,527 chars, 16 headings, 0 tables | 1.88 s / 0.05 s | |
| simple-oauth2-1593ce4a.html | trafilatura / strip tags | 13 | 30,758 chars, 23 headings, 0 tables | 41,152 chars, 20 headings, 0 tables | 1.46 s / 0.04 s | |
| query-params-str-validations-22be137a.html | trafilatura / strip tags | 10 | 27,024 chars, 22 headings, 0 tables | 36,479 chars, 3 headings, 0 tables | 7.28 s / 0.04 s | |
| bigger-applications-18edb09b.html | trafilatura / strip tags | 9 | 24,470 chars, 23 headings, 0 tables | 32,391 chars, 0 headings, 0 tables | 0.98 s / 0.07 s | |
<!-- parsers:end -->

### D07 · Parsing my corpus

- Files in the manifest: ___ · parsed: ___ · failed: ___ · pages in Postgres: ___
- Parsing coverage: ___ % of files

### Failures by reason

| Reason | Files | What I did |
|---|---|---|
| | | |

- The one I fixed: file ________ , reason ________ , fix: ________

### What I saw when I read my parsed pages

- A page where the heading path is right (document, page, path):
- Something that came out wrong (document, page, what):
- A table: Markdown grid or loose text? (document, page):

### My parser choice

- For PDFs I use ________ because (2 lines, with numbers from the table above):
- A kind of document in my corpus that neither parser handles well:

### One thing that went wrong today, and how I fixed it
