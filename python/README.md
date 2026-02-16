# Python + Streamlit RAG Workshop

Build a RAG-powered documentation assistant using **Python**, **Streamlit**, and **Gemini File Search**. Perfect for MLH Global Hack Week!

## 🎯 What You'll Build

A chatbot that answers questions about MLH's documentation with **zero hallucinations** — every answer is grounded in your actual docs and includes citations.

**Tech Stack:**
- **Backend:** Python 3.10+ with `google-genai` SDK
- **UI:** Streamlit (instant chat interface, no React needed)
- **RAG:** Gemini File Search (automatic chunking, embeddings, retrieval)
- **Docs:** MLH hackathon guides, policies, and FAQs

## 📚 Workshop Materials

| File | Description |
|------|-------------|
| **[STREAM_PLAN.md](STREAM_PLAN.md)** | Detailed 2-hour stream plan with timestamps, code, and talking points |
| **[docs/WORKSHOP.md](docs/WORKSHOP.md)** | Step-by-step tutorial for following along |
| **[finished/](finished/)** | Complete working implementation (reference or quick start) |

## 🚀 Quick Start

Want to skip ahead and see it working?

```bash
cd finished/
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY to .env
python setup_store.py
streamlit run app.py
```

See [finished/README.md](finished/README.md) for details.

## 📖 Learning Path

### For Live Stream (2 hours)

Follow [STREAM_PLAN.md](STREAM_PLAN.md) — includes:
- What RAG is and why it matters
- How Gemini File Search works
- Live coding from scratch
- Common pitfalls and debugging tips
- Q&A time

### For Self-Paced Learning

Follow [docs/WORKSHOP.md](docs/WORKSHOP.md) — includes:
- Prerequisites and setup
- Every code snippet with explanations
- Expected output at each step
- "Try it yourself" challenges
- Troubleshooting section

## 🎓 What You'll Learn

### RAG Concepts
- What is Retrieval-Augmented Generation?
- How chunking, embeddings, and vector search work
- Why RAG solves LLM hallucination problems

### Gemini File Search
- Creating and managing FileSearchStores
- Uploading and indexing documents
- Querying with automatic retrieval
- Extracting citations from responses

### Streamlit Basics
- `st.chat_input` and `st.chat_message` for chat UI
- Session state for conversation history
- Streaming responses for better UX
- Sidebar controls and example questions

### Production Patterns
- Environment variable management
- Error handling and loading states
- Streaming vs non-streaming responses
- Citation display and UX

## 📋 Prerequisites

- **Python 3.10+** (check with `python --version`)
- **pip** package manager
- **Google AI Studio API key** (free): [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Basic Python knowledge (functions, loops, imports)
- No AI/ML experience required!

## 🏗️ Project Structure

```
python/
├── STREAM_PLAN.md              # Presenter's guide (2-hour plan)
├── docs/
│   └── WORKSHOP.md             # Student tutorial (step-by-step)
├── finished/                   # Reference implementation
│   ├── app.py                  # Streamlit chat app
│   ├── setup_store.py          # Create FileSearchStore + upload docs
│   ├── query_test.py           # CLI testing tool
│   ├── requirements.txt        # Dependencies
│   ├── .env.example            # Environment template
│   └── README.md               # Usage instructions
└── README.md                   # This file
```

## 🎬 The Demo

Ask questions like:
- "How do I get reimbursed for a Hack Day?"
- "What are the requirements to be an MLH member event?"
- "What is MLH's code of conduct?"

Get **accurate answers with citations** showing exactly where the info came from.

## 🔧 Customization

After the workshop, swap in your own docs:

**Your company's internal knowledge base:**
```python
MY_DOCS = {
    "api-guide.md": "https://raw.githubusercontent.com/yourorg/docs/main/api.md",
    "faq.md": "https://raw.githubusercontent.com/yourorg/docs/main/faq.md",
}
```

**Your project README:**
```python
MY_DOCS = {
    "README.md": "https://raw.githubusercontent.com/you/project/main/README.md",
}
```

**Your school's handbook:**
```python
# Convert PDF → Markdown first, then upload
MY_DOCS = {
    "student-handbook.md": "./path/to/handbook.md",
}
```

The same code works for **any documentation** — just point it at different files!

## 🌟 Why This Workshop?

### For Learners
- Understand RAG from first principles
- Build something practical in 2 hours
- No ML PhD required
- Deploy-ready code

### For Hackers
- Perfect for documentation tools
- Internal knowledge base bots
- Customer support automation
- Research paper Q&A

### For Organizers
- Ready-to-stream content
- Detailed speaker notes
- Beginner-friendly
- Active learning (live coding)

## 🤝 Contributing

This workshop is open source! Found a bug? Have an improvement?

1. Fork the repo
2. Create a feature branch
3. Submit a PR

Ideas we'd love:
- More example docs to index
- Additional Streamlit UI features
- Deployment guides (Docker, Railway, etc.)
- Video walkthrough links

## 📚 Resources

### Gemini API
- [File Search Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- [API Reference](https://ai.google.dev/api/rest)
- [Get API Key](https://aistudio.google.com/apikey)
- [Python SDK Docs](https://googleapis.github.io/python-genai/)

### Streamlit
- [Streamlit Docs](https://docs.streamlit.io/)
- [Chat Elements Guide](https://docs.streamlit.io/develop/api-reference/chat)
- [Deployment Options](https://docs.streamlit.io/deploy)

### MLH
- [MLH on GitHub](https://github.com/MLH)
- [Global Hack Week](https://ghw.mlh.io/)
- [MLH Fellowship](https://fellowship.mlh.io/)

### RAG Background
- [What is RAG? (Google Cloud)](https://cloud.google.com/use-cases/retrieval-augmented-generation)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)
- [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

## 🎉 Let's Build!

Ready to start? Pick your path:

- **Live stream:** Open [STREAM_PLAN.md](STREAM_PLAN.md)
- **Self-paced:** Open [docs/WORKSHOP.md](docs/WORKSHOP.md)
- **Quick demo:** `cd finished/` and follow the README

Questions? Open an issue or ask in the MLH Discord!

---

**Made with ❤️ for MLH Global Hack Week**
