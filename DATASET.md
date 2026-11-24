# Dataset: PassportPal

PassportPal is a passport assistance project that provides personalised passport document checklists and answers questions about annexures, Tatkal applications, police verification, and passport fees.

## Dataset targets

- **Start target:** Official passport instructions, FAQs, and annexures.
- **Full target:** Start target plus passport rules, circulars, and fee schedules, targeting 800+ pages.
- **Current status:** Initial collection completed. The collected files include official passport-related sources and additional technical reference material. The start target still requires a coverage review to confirm that all required passport instructions, FAQs, and annexures are included.

## Collection method

Documents were collected using `scripts/fetch.py`.

- **Repository:** https://github.com/darshini171006-commits/prince28-cit03-passportpal
- **User-Agent:** `examate-student-bot`
- **Maximum concurrent requests:** 4
- **Delay between requests to the same host:** 0.5 seconds
- **Robots.txt:** Checked before crawling.
- **Retries:** Temporary network and server errors are retried with backoff and jitter.
- **Manifest:** `data/manifest.jsonl` records downloaded files and their metadata.

## Sources

The main passport information sources are:

- https://www.passportindia.gov.in/
- https://www.mea.gov.in/

Additional technical reference sources:

- https://fastapi.tiangolo.com/tutorial/
- https://github.com/D1vyanshu1/Government-Service-RAG-chatbot

The FastAPI and Government-Service-RAG materials are technical references. They are not authoritative sources for Indian passport rules or procedures.

## Dataset summary

**Collection snapshot: 23 November 2026**

| Source | Files | Size (MB) | Estimated pages |
|---|---:|---:|---:|
| FastAPI technical documentation | 51 | 8.0 | 252 |
| Government-Service-RAG repository | 2 | 0.0 | 5 |
| Ministry of External Affairs (MEA) | 1 | 2.4 | 28 |
| Passport Seva / Passport India | 9 | 4.1 | 78 |
| **Total** | **63** | **14.5** | **363** |

- Downloaded files: 63
- Blocked by robots.txt: 0
- Failed downloads: 0
- Total collected size: approximately 14.5 MB
- Estimated pages: 363

*Page counts are estimates. PDF page counts are used where available; text and HTML pages are estimated at one page per 3,000 characters.*

## Licence and usage considerations

The presence of a publicly accessible document does not automatically mean that it is public domain or freely reusable.

- **Passport India:** Official government information. Applicable reuse and reproduction terms require verification.
- **MEA:** Official government legislation. Applicable reuse and reproduction terms require verification.
- **FastAPI:** Refer to the licence and terms applicable to the FastAPI documentation and repository.
- **Government-Service-RAG:** Refer to the repository's licence and terms.

Until permissions are verified, the project should treat these materials as reference sources and link users to the original documents.

Every passport-related answer should provide a link to its original official source wherever possible. The project should not collect unnecessary personal information.

## Dataset inventory

The complete file inventory, including source URLs, file paths, download status, and SHA-256 fingerprints, is maintained in:

`data/manifest.jsonl`

The generated collection report can be refreshed using:

```powershell
uv run python scripts/dataset_report.py
```

## Known gaps

- The current collection contains only 10 files from the Passport India and MEA source groups. These need to be checked against the complete list of required passport instructions, FAQs, and annexures.
- The full target of 800+ pages has not yet been reached. The current dataset contains approximately 363 estimated pages across all sources.
- Additional official passport circulars, updated fee schedules, and relevant rules may still need to be collected.
- Some HTML pages do not have a reliable page count because they are web pages rather than PDFs.
- Reuse permissions for the official government sources have not yet been fully verified.
- The dataset should be reviewed periodically to identify outdated documents and replace them with current official versions.

## Next steps

1. Review the collected Passport India and MEA documents against the start target.
2. Identify missing official FAQs, annexures, instructions, and relevant passport documents.
3. Verify applicable source licences and reuse conditions.
4. Expand the collection towards the full 800+ page target.
5. Regenerate the dataset report after each collection update.
