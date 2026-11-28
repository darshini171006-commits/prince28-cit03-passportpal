# Capacity plan

The following measurements are based on the actual downloaded corpus. Estimates for the 800-page target are projections, not actual database usage or provider billing. Verify storage and embedding usage against the deployed services.

<!-- generated:start -->
## Measured on my start corpus (2026-11-28 04:46 UTC)

| What | Value |
|---|---|
| Files | 6 |
| Size on disk | 6.6 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 120 |
| Characters of text | 148,260 |
| Estimated tokens (characters / 4) | 37,065 |
| Tokens per page | 309 |
| PDFs with almost no text (scanned? OCR is Day 7) | 2 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 800 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 6.7 |
| Tokens | measured tokens x scale | 0.25 M |
| Raw files | measured MB x scale | 44 MB |
| Chunks | tokens / 400 x 1.15 overlap | 710 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.04 = Rs 4 |
| Vector storage | chunks x 768 numbers x 4 bytes | 2 MB |
| Text in Postgres | characters x scale x 1.2 | 1 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->
