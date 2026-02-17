# MLH Gemini RAG Workshop

Build a RAG-powered doc assistant with [Gemini File Search](https://ai.google.dev/gemini-api/docs/file-search) for [MLH Global Hack Week](https://ghw.mlh.io/).

## What You'll Build

A chatbot that can answer questions about MLH's documentation using **Retrieval-Augmented Generation (RAG)**. Upload docs, ask questions, get accurate answers with citations — no hallucinations.

The same technique works with **any** documentation. Swap in your own docs after the workshop!

## Workshop: Python + Streamlit

| | Details |
|---|---|
| **Folder** | [`python/`](./python/) |
| **Stack** | Python 3.10+, Streamlit, `google-genai` SDK |
| **UI** | Streamlit chat components (chat interface in 10 lines!) |
| **Best For** | Learning RAG concepts deeply, rapid prototyping |
| **Deploy** | `streamlit run app.py` (or Streamlit Cloud for free hosting) |

## Demo Corpus: MLH Resources

The workshop uses these MLH docs as the knowledge base:

- [MLH Hackathon Organizer Guide](https://github.com/MLH/mlh-hackathon-organizer-guide) (organizer guide chapters, timeline, sponsorship, judging, community values)
- [MLH Policies](https://github.com/MLH/mlh-policies/tree/main) (code of conduct, community values)
- [MLH Hack Days Organizer Guide](https://github.com/MLH/mlh-hack-days-organizer-guide)

## What is RAG?

**Retrieval-Augmented Generation** solves a core LLM problem: models don't know about your private docs and can hallucinate when asked about them.

RAG works in 3 steps:
1. **Index** — Split your docs into chunks, convert to embeddings (numerical vectors), store in a vector database
2. **Retrieve** — When a user asks a question, find the most relevant chunks via semantic search
3. **Generate** — Feed the retrieved chunks to the LLM as context, generating an accurate, grounded answer

**Gemini File Search** handles all of this automatically — no external vector database, no chunking logic, no embedding pipeline. Upload files, query, done.

## Prerequisites

- A [Google AI Studio](https://aistudio.google.com/) account and API key (free)
- Python 3.10+, pip
- No AI/ML experience required!

## Getting Started

```bash
# Clone the repo
git clone https://github.com/wei/mlh-gemini-rag-workshop.git
cd mlh-gemini-rag-workshop/python

# Follow the STREAM_PLAN.md or docs/WORKSHOP.md
```

## Quick Demo

```bash
cd python/finished/
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY to .env
python setup_store.py
streamlit run app.py
```

## License

MIT
