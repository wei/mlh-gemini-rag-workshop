# MLH RAG Assistant - Finished Version

This is the complete, working version of the RAG-powered documentation assistant.

## What It Does

Ask questions about MLH documentation and get accurate, cited answers using:
- **Next.js 15** for the app framework
- **Vercel AI SDK** for streaming chat
- **Gemini 2.0 Flash** as the LLM
- **Gemini File Search** for RAG (retrieval-augmented generation)

## Prerequisites

- Node.js 18+ and npm
- A [Google AI Studio](https://aistudio.google.com/) API key

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Google AI API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here
FILE_SEARCH_STORE_NAME=mlh-docs-store
```

### 3. Create the FileSearchStore

This downloads MLH docs, uploads them to Google AI, and indexes them:

```bash
npm run setup-store
```

This will:
- ✅ Create a FileSearchStore named `mlh-docs-store`
- 📥 Download MLH documentation from GitHub
- 📤 Upload to Google AI
- ⏳ Wait for indexing to complete (~30-60 seconds)
- 🧪 Test with a sample query

**You only need to run this once!** The store persists in your Google AI account.

### 4. Run the App

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
finished/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Main chat page (useChat hook)
│   ├── globals.css             # Global styles + Tailwind
│   └── api/
│       └── chat/
│           └── route.ts        # API route (streamText + fileSearch)
├── components/
│   ├── chat-message.tsx        # Message bubble component
│   └── citation.tsx            # Expandable citation display
├── lib/
│   └── store.ts                # Shared store config
├── scripts/
│   └── setup-store.ts          # Store setup script
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
├── postcss.config.mjs
└── .env.example
```

## How It Works

### Architecture Flow

```
User Browser → useChat Hook → POST /api/chat → streamText + fileSearch → Gemini 2.0 → FileSearchStore
                    ↑                                                              ↓
                    └──────────────────── Streaming Response ──────────────────────┘
```

### Key Components

1. **`app/page.tsx`** — Client component using `useChat()` hook
   - Manages chat state
   - Handles streaming responses
   - Renders messages with citations

2. **`app/api/chat/route.ts`** — Server API route
   - Uses `streamText` from Vercel AI SDK
   - Configures Gemini model with fileSearch tool
   - Streams responses back to client

3. **`scripts/setup-store.ts`** — One-time setup
   - Creates FileSearchStore
   - Downloads and uploads MLH docs
   - Waits for indexing

4. **`components/`** — Reusable UI components
   - `chat-message.tsx` — Message bubbles
   - `citation.tsx` — Expandable source citations

## Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel deploy --prod
```

Add your `GOOGLE_API_KEY` and `FILE_SEARCH_STORE_NAME` as environment variables in the Vercel dashboard.

## Troubleshooting

### "Store not found" error

Make sure you ran `npm run setup-store` first. The store name in `.env` must match what the script created.

### API key errors

- Get your key from [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Make sure it's in your `.env` file as `GOOGLE_API_KEY`
- Restart the dev server after updating `.env`

### Indexing takes too long

The setup script waits up to 5 minutes. If it times out:
- Check your internet connection
- Verify the API key has access to Gemini File Search
- Try running the script again

### No citations showing up

Citations come from the `fileSearch` tool invocation results. They should appear automatically when the model uses the tool. If not:
- Verify the store is ACTIVE (run setup-store again)
- Check that the store name matches in `.env`
- Look for errors in the browser console

## Learn More

- [Vercel AI SDK Docs](https://sdk.vercel.ai/docs)
- [Gemini File Search Guide](https://ai.google.dev/gemini-api/docs/file-search)
- [Next.js Documentation](https://nextjs.org/docs)

## Next Steps

Want to customize this for your own docs?

1. Edit `lib/store.ts` — Change `MLH_DOCS` to your document URLs
2. Run `npm run setup-store` to create a new store
3. Update the system prompt in `app/api/chat/route.ts`

That's it! You now have a RAG assistant for your documentation.
