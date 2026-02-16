# MLH Gemini RAG Workshop

Build a RAG-powered doc assistant with [Gemini File Search](https://ai.google.dev/gemini-api/docs/file-search) — two complete workshops for [MLH Global Hack Week](https://ghw.mlh.io/).

## What You'll Build

A chatbot that can answer questions about MLH's documentation using **Retrieval-Augmented Generation (RAG)**. Upload docs, ask questions, get accurate answers with citations — no hallucinations.

The same technique works with **any** documentation. Swap in your own docs after the workshop!

## Two Workshops

| | Python + Streamlit | Next.js + Vercel AI SDK |
|---|---|---|
| **Folder** | [`python/`](./python/) | [`javascript/`](./javascript/) |
| **Stack** | Python, Streamlit, `google-genai` SDK | Next.js, Vercel AI SDK, `@ai-sdk/google` |
| **UI** | Streamlit chat components | React + `useChat` hook + Tailwind CSS |
| **Best For** | Learning RAG concepts deeply | Building a production-ready web app |
| **Deploy** | `streamlit run app.py` | `vercel deploy` → live URL |

Each workshop is **self-contained** — no need to do both or in any order.

## Demo Corpus: MLH Resources

Both workshops use these MLH docs as the knowledge base:

- [MLH Hackathon Organizer Guide](https://github.com/MLH/mlh-hackathon-organizer-guide)
- [MLH Policies](https://github.com/MLH/mlh-policies/tree/main)
- [MLH Hack Days Organizer Guide](https://github.com/MLH/mlh-hack-days-organizer-guide)
- [MLH Fellowship FAQ](https://mlh.link/fellowship-faq)

## What is RAG?

**Retrieval-Augmented Generation** solves a core LLM problem: models don't know about your private docs and can hallucinate when asked about them.

RAG works in 3 steps:
1. **Index** — Split your docs into chunks, convert to embeddings (numerical vectors), store in a vector database
2. **Retrieve** — When a user asks a question, find the most relevant chunks via semantic search
3. **Generate** — Feed the retrieved chunks to the LLM as context, generating an accurate, grounded answer

**Gemini File Search** handles all of this automatically — no external vector database, no chunking logic, no embedding pipeline. Upload files, query, done.

## Prerequisites

- A [Google AI Studio](https://aistudio.google.com/) account and API key
- **Python workshop:** Python 3.10+, pip
- **JavaScript workshop:** Node.js 18+, npm

## Getting Started

```bash
# Clone the repo
git clone https://github.com/wei/mlh-gemini-rag-workshop.git
cd mlh-gemini-rag-workshop

# Choose your workshop
cd python/    # or cd javascript/

# Follow the STREAM_PLAN.md in each folder
```

## License

MIT
