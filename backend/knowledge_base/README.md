Place company knowledge-base documents (PDF, DOCX, TXT, or Markdown) here.
The FAQ agent searches these local documents and gives the matching excerpts to the configured LLM to produce a grounded answer with a source filename.

The sample `company_policy.docx` is included. Documents are loaded on the first FAQ request and cached while the backend runs. Restart the backend after adding or changing files so the FAQ agent reloads them. The supplied NovaOne PDF describes a fictional company; use it for testing only and replace it with your approved business documentation before serving real customers.
