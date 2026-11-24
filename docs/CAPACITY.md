## What I conclude

1. **Embedding cost:** Embedding the estimated 800-page corpus costs approximately $0.08 (INR 8) one time, so embedding cost is not a major concern for this project.

2. **Storage:** The estimated vector storage is 4 MB and text storage is 2 MB. Together, they require approximately 6 MB. I will compare this with the actual storage limit and usage shown on my PostgreSQL dashboard before confirming capacity.

3. **Least certain estimate:** The estimated tokens per page (612) may vary depending on document formatting and content. I can improve accuracy by measuring actual token counts after extracting and tokenizing the documents.

4. **If the corpus grows 10 times:** Storage and processing requirements will increase approximately tenfold, assuming similar document sizes. I will need to monitor database storage, embedding costs, indexing performance, and retrieval speed as the dataset grows.
