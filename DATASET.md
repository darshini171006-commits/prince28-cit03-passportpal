# Dataset: PassportPal

PassportPal provides passport document checklists and answers questions about Indian passport procedures, annexures, Tatkal applications, police verification, and fees.

## Dataset status

- Current corpus: 6 official government PDF documents.
- Measured coverage: 120 pages.
- Full target: 800 pages.
- The 800-page target has not yet been reached.

## Sources

- Passport Seva / Passport India: official passport service information.
- Ministry of External Affairs (MEA): official passport legislation and rules.

Only official passport-related documents are included. Unrelated FastAPI and Government-Service-RAG materials have been removed.

## Collection files

- Source list: `data/sources.csv`
- Fetcher: `scripts/fetch.py`
- Download manifest: `data/manifest.jsonl`
- Dataset report: `scripts/dataset_report.py`

Public accessibility does not automatically grant permission to reproduce or redistribute documents. Verify applicable reuse terms and link users to original official sources.

## Known gaps

- More official FAQs and usable annexures are needed.
- Additional circulars and updated fee schedules may be required.
- Two PDFs need OCR and extraction-quality review.
- The corpus must be expanded towards 800 pages.

## Next steps

1. Collect official Passport Seva FAQs and annexures.
2. Add verified URLs to `data/sources.csv`.
3. Fetch and validate documents.
4. Review OCR and extraction quality.
5. Regenerate the dataset report.

<!-- generated:start -->
## Sources (generated 2026-11-28 04:46 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| mea | Official government legislation; verify applicable reuse terms | 2 | 2.6 | 42 | http | 2026-11-25 | https://www.mea.gov.in/images/pdf/passport1980.pdf |
| passportindia | Official government information; reuse permission pending verification | 4 | 4.1 | 78 | http | 2026-11-23 | https://passportindia.gov.in/AppOnlineProject/pdf/Citizen_Charter.pdf |

**Total:** 6 files, 6.6 MB, 120 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 6 of 6)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | The Passports Act 1967 | mea | 14 | 2026-11-25 | https://www.mea.gov.in/Uploads/PublicationDocs/140_The-Passport-Act-1967.pdf |
| 2 | Passports Rules 1980 | mea | 28 | 2026-11-23 | https://www.mea.gov.in/images/pdf/passport1980.pdf |
| 3 | Application Form Instruction Booklet | passportindia | 21 | 2026-11-23 | https://www.passportindia.gov.in/AppOnlineProject/pdf/ApplicationformInstructionBooklet-V3.0.pdf |
| 4 | Citizen Charter | passportindia | 11 | 2026-11-23 | https://passportindia.gov.in/AppOnlineProject/pdf/Citizen_Charter.pdf |
| 5 | Steps to Apply for Passport Services | passportindia | 29 | 2026-11-23 | https://passportindia.gov.in/AppOnlineProject/pdf/steps_to_apply_for_passport_services.pdf |
| 6 | Steps to Submit Application at PSK | passportindia | 17 | 2026-11-23 | https://www.passportindia.gov.in/AppOnlineProject/pdf/Steps_to_Submit_an_Application_at_PSK.pdf |
<!-- generated:end -->
