# JavaScript Workshop: Build a RAG-Powered Doc Assistant with Next.js + Vercel AI SDK

**Duration:** 2 hours  
**Level:** Intermediate  
**Format:** Live coding workshop for [MLH Global Hack Week](https://ghw.mlh.io/)

---

## What You'll Build

A production-ready **RAG-powered documentation assistant** that answers questions about MLH documentation with accurate, cited responses.

**Tech Stack:**
- ⚡ **Next.js 15** - App Router, Server Components, API Routes
- 🤖 **Vercel AI SDK** - Streaming chat, React hooks
- 🔍 **Gemini File Search** - RAG without a vector database
- 🎨 **Tailwind CSS** - Modern, responsive UI
- 📘 **TypeScript** - Type-safe development

**See it in action:** [Live demo](https://mlh-rag-assistant.vercel.app) *(coming soon)*

---

## Why This Workshop?

### 🚀 Production-Ready

This isn't a toy demo - it's a real app you can:
- Deploy to Vercel in minutes
- Customize for your own docs
- Show to recruiters/employers
- Use in hackathon projects

### 🎯 Practical RAG

Learn RAG (Retrieval-Augmented Generation) without the complexity:
- No vector database setup
- No embedding models to manage
- No chunking strategies to optimize
- **Just upload docs and go**

### ⚡ Modern Stack

Use the latest tools:
- Next.js 15 App Router
- React Server Components
- Streaming responses
- Type-safe APIs

---

## Prerequisites

### Required

- **Node.js 18+** and npm
  ```bash
  node --version  # Should be 18 or higher
  ```

- **Google AI Studio API Key**
  - Get it here: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
  - Free tier is generous (60 requests/minute)

### Helpful

- Basic React/Next.js knowledge
- Familiarity with TypeScript
- Understanding of REST APIs

---

## Quick Start

### Option 1: Follow the Live Stream

**When:** [Check MLH Global Hack Week schedule](https://ghw.mlh.io/)

Watch the 2-hour live coding session where we build this from scratch. Follow along in real-time!

### Option 2: Self-Paced Tutorial

Follow the step-by-step guide:

```bash
# Read the workshop guide
cat docs/WORKSHOP.md

# Or view it on GitHub
open https://github.com/wei/mlh-gemini-rag-workshop/blob/main/javascript/docs/WORKSHOP.md
```

The workshop includes:
- Detailed explanations
- Code snippets you can copy-paste
- Troubleshooting tips
- Expected output at each step

### Option 3: Use the Finished Code

Jump straight to the working app:

```bash
cd finished/
npm install
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
npm run setup-store
npm run dev
```

See [`finished/README.md`](./finished/README.md) for details.

---

## What's Included

```
javascript/
├── STREAM_PLAN.md              # Detailed 2-hour stream plan
├── docs/
│   └── WORKSHOP.md             # Step-by-step tutorial
├── finished/                   # Complete working app
│   ├── app/                    # Next.js app
│   ├── components/             # React components
│   ├── lib/                    # Shared utilities
│   ├── scripts/                # Setup scripts
│   └── README.md               # How to run
└── README.md                   # This file
```

---

## Workshop Outline

### Part 1: Introduction (10 min)

- Welcome & context
- Show the finished demo
- Explain what RAG is and why it matters

### Part 2: RAG Overview (15 min)

- How RAG works (Retrieve → Augment → Generate)
- Traditional RAG vs Gemini File Search
- Architecture diagram

### Part 3: Project Setup (15 min)

- Create Next.js app
- Install AI SDK packages
- Configure environment variables

### Part 4: FileSearchStore Setup (20 min)

- Write setup script
- Download MLH docs
- Upload to Google AI
- Wait for indexing
- Test with a query

### Part 5: Build the API (20 min)

- Create `/api/chat` route
- Use `streamText()` from AI SDK
- Configure fileSearch tool
- Test with curl

### Part 6: Build the UI (20 min)

- Use `useChat()` hook
- Create message components
- Add citation display
- Style with Tailwind

### Part 7: Deploy (10 min)

- Deploy to Vercel
- Add environment variables
- Share live URL

### Part 8: Wrap Up (10 min)

- Recap what we built
- Next steps and challenges
- Q&A

---

## Key Concepts

### RAG (Retrieval-Augmented Generation)

**The Problem:** LLMs don't know about your private docs.

**The Solution:**
1. **Index** your docs in a vector database
2. **Retrieve** relevant chunks when asked a question
3. **Generate** an answer using the LLM + retrieved context

**Result:** Accurate, grounded answers with no hallucinations.

### Vercel AI SDK

A unified toolkit for building AI applications:

- **`streamText()`** - Stream LLM responses
- **`useChat()`** - React hook for chat UIs
- **Provider abstraction** - Switch between OpenAI, Anthropic, Google, etc.
- **Tool calling** - Enable function execution

### Gemini File Search

Google's managed RAG solution:

- Upload files → automatic embeddings
- Managed vector store → no infrastructure
- Integrated with Gemini → one API
- Citation tracking → see source chunks

---

## Architecture

```
┌─────────────────────┐
│   Browser (React)   │
│   ┌─────────────┐  │
│   │ useChat()   │  │  Manages state, streaming
│   └─────────────┘  │
└─────────┬───────────┘
          │ POST /api/chat
          ▼
┌─────────────────────┐
│  Next.js API Route  │
│   ┌─────────────┐  │
│   │ streamText()│  │  Calls Gemini with fileSearch
│   └─────────────┘  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│    Gemini API       │
│   ┌─────────────┐  │
│   │ File Search │  │  Retrieves relevant docs
│   │   Store     │  │
│   └─────────────┘  │
└─────────────────────┘
```

---

## Learning Outcomes

After this workshop, you'll know how to:

✅ Build a streaming chat API with the Vercel AI SDK  
✅ Implement RAG using Gemini File Search  
✅ Create real-time UIs with the `useChat()` hook  
✅ Deploy full-stack Next.js apps to Vercel  
✅ Handle citations and source tracking  
✅ Customize for your own documentation

---

## Customization Ideas

### Use Your Own Docs

1. Edit `lib/store.ts` - change document URLs
2. Run `npm run setup-store` - index your docs
3. Update system prompt - guide the assistant
4. Deploy - you're done!

**Works with:**
- Company wikis
- Product documentation
- Legal documents
- Academic papers
- Blog posts
- Anything in text/markdown/PDF

### Add Features

- 🎤 Voice input (Web Speech API)
- 🔊 Audio output (ElevenLabs, Google TTS)
- 🖼️ Image uploads (multimodal queries)
- 📊 Analytics (track popular questions)
- 👤 Authentication (user accounts)
- 💾 Conversation history (save/export)
- 🌍 Multi-language support

### Style It

- Custom branding and colors
- Light/dark mode toggle
- Mobile-responsive design
- Animated transitions
- Custom fonts and typography

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| API key error | Get key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| Store not found | Run `npm run setup-store` first |
| Build fails | Check `npm run build` output for errors |
| No citations | Verify store is ACTIVE state |
| Slow indexing | Wait up to 5 minutes, check internet connection |

See [`docs/WORKSHOP.md`](./docs/WORKSHOP.md) for detailed troubleshooting.

---

## Resources

### Documentation

- [Vercel AI SDK](https://sdk.vercel.ai/docs) - Official AI SDK docs
- [Gemini File Search](https://ai.google.dev/gemini-api/docs/file-search) - Google's RAG guide
- [Next.js App Router](https://nextjs.org/docs/app) - Next.js 13+ docs
- [Tailwind CSS](https://tailwindcss.com/docs) - Styling framework

### Example Projects

- [Vercel AI SDK Examples](https://github.com/vercel/ai) - Official examples
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples) - Next.js starters
- [MLH Workshops](https://github.com/MLH) - More MLH resources

### Community

- [MLH Discord](https://discord.mlh.io/) - Get help from MLH community
- [Vercel Discord](https://vercel.com/discord) - AI SDK support
- [Next.js Discussions](https://github.com/vercel/next.js/discussions) - Next.js Q&A

---

## Challenge: Build Your Own

**Task:** Adapt this workshop for a different use case.

**Requirements:**
- At least 5 documents in your store
- Custom branding and styling
- Unique system prompt
- Deployed to Vercel
- Shared in MLH Discord

**Ideas:**
- Recipe recommendation bot
- Legal Q&A assistant
- Academic paper explorer
- Product documentation helper
- Travel guide chatbot

**Share your project:** Use `#mlh-ghw-rag` in Discord!

---

## Credits

**Workshop Creator:** [Wei He](https://github.com/wei)  
**Event:** [MLH Global Hack Week](https://ghw.mlh.io/)  
**Powered by:**
- [Vercel AI SDK](https://sdk.vercel.ai/)
- [Google Gemini](https://ai.google.dev/)
- [Next.js](https://nextjs.org/)

---

## License

MIT - feel free to use this code for your hackathon projects!

---

## Next Steps

Ready to start?

1. **Live Stream:** Watch the 2-hour coding session
2. **Tutorial:** Follow [`docs/WORKSHOP.md`](./docs/WORKSHOP.md)
3. **Finished Code:** Explore [`finished/`](./finished/)
4. **Stream Plan:** Reference [`STREAM_PLAN.md`](./STREAM_PLAN.md)

**Questions?** Open an issue or ask in [MLH Discord](https://discord.mlh.io/)

**Let's build something awesome! 🚀**
