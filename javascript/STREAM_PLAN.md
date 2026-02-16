# Stream Plan: Build a RAG-Powered Doc Assistant (Next.js + Vercel AI SDK)

**Duration:** 2 hours  
**Format:** Live coding workshop  
**Target:** MLH Global Hack Week participants

---

## Pre-Stream Checklist

- [ ] Test finished demo app - make sure it works end-to-end
- [ ] Have `.env` file ready with valid API key
- [ ] Clear browser cache and terminal history
- [ ] Open tabs: GitHub repo, AI Studio, Vercel AI SDK docs
- [ ] Test screen share and audio
- [ ] Have a glass of water nearby
- [ ] Pin important commands to a notes file

---

## 0:00–0:10 | Intro & Context (10 min)

### Talking Points

**Welcome & Setup (2 min)**
- "Hey everyone! Welcome to MLH Global Hack Week!"
- "I'm [name] and today we're building something practical you can use in your hackathon projects"
- "If you're just joining, drop a 👋 in chat - let's see where everyone's from!"

**Show the Finished Demo (3 min)**
- Screen share: Open the finished app running on localhost:3000
- "This is what we're building today - a RAG-powered documentation assistant"
- Ask it a question live: "What are the key responsibilities of an MLH hackathon organizer?"
- Point out:
  - Streaming response (appears word by word)
  - Citations that expand to show source text
  - Clean, modern UI
- "The magic here is RAG - Retrieval-Augmented Generation"

**What We're Building (5 min)**
- "Three key pieces:"
  1. A Next.js app with a chat interface
  2. Gemini File Search for RAG (no vector DB needed!)
  3. Vercel AI SDK to glue it all together
- "Why Next.js? It's production-ready, deploys to Vercel in one command, and the AI SDK makes streaming dead simple"
- "Why Gemini File Search? It handles embeddings, chunking, and indexing automatically - you just upload docs"
- "By the end, you'll have a working app you can deploy and show to recruiters"

### Common Pitfalls
- Don't spend too long on theory - get to building fast
- If chat is slow, acknowledge it and move on
- Have the finished app open in a separate window in case you need to reference it

### Transition
"Alright, let's look at how RAG actually works before we start coding"

---

## 0:10–0:25 | RAG + Architecture Overview (15 min)

### Talking Points

**What is RAG? (5 min)**
- "RAG stands for Retrieval-Augmented Generation"
- "The problem: LLMs don't know about YOUR docs. If you ask GPT about your company's internal wiki, it'll either hallucinate or say 'I don't know'"
- "RAG fixes this in 3 steps:"
  1. **Index** - Split docs → embeddings (vectors) → vector database
  2. **Retrieve** - User question → find relevant chunks via semantic search
  3. **Generate** - Feed chunks to LLM as context → grounded answer
- Draw on screen (or show slide):
  ```
  User Question
       ↓
  [Vector Search] ← Vector DB (your docs)
       ↓
  Relevant Chunks
       ↓
  [LLM] → Grounded Answer + Citations
  ```

**Our Stack (5 min)**
- "Normally you'd need:"
  - Embedding model (OpenAI, Cohere)
  - Vector database (Pinecone, Weaviate, pgvector)
  - Chunking logic
  - Indexing pipeline
- "With Gemini File Search: upload files, done. Google handles the rest."
- "The Vercel AI SDK sits in the middle:"
  - Abstracts away streaming
  - Unified interface for different providers
  - Built-in React hooks (`useChat`)

**Architecture Diagram (5 min)**
- Draw the full flow:
  ```
  Browser (React)
       ↓
  useChat() hook
       ↓
  POST /api/chat
       ↓
  streamText()
       ├─ model: google('gemini-2.0-flash')
       └─ tools: { fileSearch }
            ↓
       Gemini API
            ↓
       FileSearchStore (MLH docs)
            ↓
       Streaming Response
            ↓
  useChat() receives chunks
       ↓
  UI updates in real-time
  ```
- "The beauty: `useChat()` on the frontend, `streamText()` on the backend, and you're streaming"

### Code to Show
None yet - just diagrams and explanation

### Common Pitfalls
- Don't get too deep into vector math
- If people ask about embeddings, say "Google handles it under the hood"
- Keep it practical and high-level

### Transition
"Enough theory - let's build this thing. First up: project setup"

---

## 0:25–0:40 | Project Setup (15 min)

### Talking Points

**Create Next.js App (5 min)**
- "Starting from scratch. Everyone can follow along."
- "If you get stuck, no worries - the finished code is in the repo"

**Install Dependencies (5 min)**
- "We need three main packages:"
  - `ai` - Vercel AI SDK (streaming, hooks)
  - `@ai-sdk/google` - Google provider for AI SDK
  - `@google/generative-ai` - Google's official SDK (for setup script)

**Environment Setup (5 min)**
- "Two env vars we need:"
  - `GOOGLE_API_KEY` - get from AI Studio
  - `FILE_SEARCH_STORE_NAME` - what we'll name our store
- Show how to get API key live:
  1. Go to aistudio.google.com/apikey
  2. Click "Create API key"
  3. Copy it

### Code to Write

```bash
# Create Next.js app
npx create-next-app@latest mlh-rag-assistant
# Select: TypeScript, Tailwind, App Router, all defaults

cd mlh-rag-assistant

# Install AI SDK packages
npm install ai @ai-sdk/google @google/generative-ai

# Dev dependency for running TypeScript scripts
npm install -D tsx
```

**Create `.env.local`:**
```bash
GOOGLE_API_KEY=your_api_key_here
FILE_SEARCH_STORE_NAME=mlh-docs-store
```

**Create `lib/store.ts`:**
```typescript
export const STORE_NAME = process.env.FILE_SEARCH_STORE_NAME || 'mlh-docs-store';

export const MLH_DOCS = [
  {
    name: 'mlh-hackathon-organizer-guide',
    url: 'https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/main/README.md',
  },
  {
    name: 'mlh-policies',
    url: 'https://raw.githubusercontent.com/MLH/mlh-policies/main/README.md',
  },
  {
    name: 'mlh-code-of-conduct',
    url: 'https://raw.githubusercontent.com/MLH/mlh-policies/main/code-of-conduct.md',
  },
  {
    name: 'mlh-community-values',
    url: 'https://raw.githubusercontent.com/MLH/mlh-policies/main/community-values.md',
  },
  {
    name: 'mlh-hack-days-guide',
    url: 'https://raw.githubusercontent.com/MLH/mlh-hack-days-organizer-guide/main/README.md',
  },
];
```

**Add to `package.json` scripts:**
```json
"setup-store": "tsx scripts/setup-store.ts"
```

### Common Pitfalls
- **Node version:** Need 18+ for Next.js 15
- **API key visibility:** Make sure `.env.local` is in `.gitignore` (it is by default)
- **Windows users:** Use `set` instead of `export` if setting env vars manually

### Expected Output
```
✓ Dependencies installed
✓ .env.local created
✓ lib/store.ts created
```

### Transition
"Setup done! Now the fun part - building the FileSearchStore and uploading our docs"

---

## 0:40–1:00 | Build the Store (20 min)

### Talking Points

**What the Setup Script Does (3 min)**
- "We're about to write a script that:"
  1. Creates a FileSearchStore in Google AI
  2. Downloads MLH docs from GitHub
  3. Uploads them to the store
  4. Waits for indexing to finish
  5. Tests with a query
- "This is a one-time setup - once the store exists, it stays in your Google AI account"

**Writing the Script (12 min)**
- "We'll use `@google/generative-ai` directly here"
- "The AI SDK doesn't expose store creation - that's fine, we use Google's SDK"
- Walk through each function:
  - `downloadFile()` - fetch from GitHub, save to tmp/
  - `createStore()` - create or get existing store
  - `uploadFiles()` - upload each doc, add to store
  - `waitForIndexing()` - poll store.state until ACTIVE
  - `testQuery()` - quick test with fileSearch tool

**Run the Script (5 min)**
- `npm run setup-store`
- Show the output as it progresses:
  - Creating store
  - Downloading files
  - Uploading (this takes a bit)
  - Waiting for indexing
  - Test query + response

### Code to Write

**Create `scripts/setup-store.ts`:**

```typescript
import { GoogleGenAI } from '@google/generative-ai';
import { STORE_NAME, MLH_DOCS } from '../lib/store';
import * as fs from 'fs';
import * as path from 'path';

const API_KEY = process.env.GOOGLE_API_KEY;

if (!API_KEY) {
  console.error('❌ GOOGLE_API_KEY environment variable is required');
  process.exit(1);
}

const genai = new GoogleGenAI(API_KEY);

async function downloadFile(url: string, filename: string): Promise<string> {
  console.log(`  📥 Downloading ${filename}...`);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to download ${url}: ${response.statusText}`);
  }
  
  const content = await response.text();
  const tmpDir = path.join(process.cwd(), 'tmp');
  
  if (!fs.existsSync(tmpDir)) {
    fs.mkdirSync(tmpDir, { recursive: true });
  }
  
  const filepath = path.join(tmpDir, filename);
  fs.writeFileSync(filepath, content, 'utf-8');
  console.log(`  ✅ Saved to ${filepath}`);
  return filepath;
}

async function createStore(name: string) {
  console.log(`\n🏗️  Creating FileSearchStore: ${name}`);
  
  try {
    const existingStore = await genai.fileSearchStores.get(name);
    console.log(`✅ Store "${name}" already exists`);
    return existingStore;
  } catch (error) {
    console.log(`  Creating new store...`);
    const store = await genai.fileSearchStores.create({
      displayName: name,
    });
    console.log(`✅ Store created: ${store.name}`);
    return store;
  }
}

async function uploadFiles(storeName: string, filepaths: string[]) {
  console.log(`\n📤 Uploading ${filepaths.length} files...`);
  
  const uploadedFiles = [];
  
  for (const filepath of filepaths) {
    const filename = path.basename(filepath);
    console.log(`  Uploading ${filename}...`);
    
    const fileContent = fs.readFileSync(filepath);
    
    const file = await genai.files.upload({
      file: {
        data: fileContent,
        mimeType: 'text/markdown',
      },
      displayName: filename,
    });
    
    console.log(`  ✅ Uploaded: ${file.name}`);
    
    await genai.fileSearchStores.addFile(storeName, file.name);
    console.log(`  ➕ Added to store`);
    
    uploadedFiles.push(file.name);
  }
  
  return uploadedFiles;
}

async function waitForIndexing(storeName: string) {
  console.log(`\n⏳ Waiting for indexing to complete...`);
  
  let attempts = 0;
  const maxAttempts = 60;
  
  while (attempts < maxAttempts) {
    const store = await genai.fileSearchStores.get(storeName);
    
    if (store.state === 'ACTIVE') {
      console.log(`✅ Indexing complete! Store is ACTIVE`);
      return;
    }
    
    console.log(`  State: ${store.state} (attempt ${attempts + 1}/${maxAttempts})`);
    
    await new Promise(resolve => setTimeout(resolve, 5000));
    attempts++;
  }
  
  throw new Error('Indexing timed out after 5 minutes');
}

async function testQuery(storeName: string) {
  console.log(`\n🧪 Testing store with a sample query...`);
  
  const model = genai.getGenerativeModel({
    model: 'gemini-2.0-flash',
    tools: [
      {
        fileSearchTool: {
          fileSearchStore: storeName,
        },
      },
    ],
  });
  
  const result = await model.generateContent(
    'What are the key responsibilities of an MLH hackathon organizer?'
  );
  
  const response = result.response;
  console.log(`\n💬 Query: What are the key responsibilities of an MLH hackathon organizer?`);
  console.log(`\n📝 Response:\n${response.text()}`);
  
  if (response.candidates?.[0]?.groundingMetadata?.groundingChunks) {
    const chunks = response.candidates[0].groundingMetadata.groundingChunks;
    console.log(`\n📚 Citations: ${chunks.length} source(s)`);
  }
}

async function main() {
  console.log('🚀 MLH RAG Store Setup\n');
  console.log(`Store name: ${STORE_NAME}`);
  console.log(`Documents: ${MLH_DOCS.length}\n`);
  
  try {
    const store = await createStore(STORE_NAME);
    
    console.log(`\n📥 Downloading MLH documentation...`);
    const filepaths: string[] = [];
    
    for (const doc of MLH_DOCS) {
      const filepath = await downloadFile(doc.url, `${doc.name}.md`);
      filepaths.push(filepath);
    }
    
    await uploadFiles(store.name, filepaths);
    await waitForIndexing(store.name);
    await testQuery(store.name);
    
    console.log(`\n🧹 Cleaning up temp files...`);
    for (const filepath of filepaths) {
      fs.unlinkSync(filepath);
    }
    fs.rmdirSync(path.join(process.cwd(), 'tmp'));
    
    console.log(`\n✨ Setup complete! Your store is ready to use.`);
    console.log(`\nNext steps:`);
    console.log(`  1. Copy .env.example to .env`);
    console.log(`  2. Add your GOOGLE_API_KEY`);
    console.log(`  3. Run: npm run dev`);
    
  } catch (error) {
    console.error(`\n❌ Setup failed:`, error);
    process.exit(1);
  }
}

main();
```

### Common Pitfalls
- **Upload takes time:** 5 docs × ~5 seconds each = 25 seconds. Warn people it's not instant
- **Indexing delay:** Usually 30-60 seconds. This is normal
- **Rate limits:** If you hit API rate limits, add delays between uploads
- **Store already exists:** The script handles this - it just reuses the existing store

### Expected Output
```
🚀 MLH RAG Store Setup

Store name: mlh-docs-store
Documents: 5

🏗️  Creating FileSearchStore: mlh-docs-store
✅ Store created: projects/.../fileSearchStores/mlh-docs-store

📥 Downloading MLH documentation...
  📥 Downloading mlh-hackathon-organizer-guide.md...
  ✅ Saved to /path/to/tmp/mlh-hackathon-organizer-guide.md
  ...

📤 Uploading 5 files...
  Uploading mlh-hackathon-organizer-guide.md...
  ✅ Uploaded: files/abc123
  ➕ Added to store
  ...

⏳ Waiting for indexing to complete...
  State: INDEXING (attempt 1/60)
  State: INDEXING (attempt 2/60)
  State: ACTIVE (attempt 3/60)
✅ Indexing complete! Store is ACTIVE

🧪 Testing store with a sample query...

💬 Query: What are the key responsibilities of an MLH hackathon organizer?

📝 Response:
MLH hackathon organizers have several key responsibilities...

📚 Citations: 3 source(s)

✨ Setup complete! Your store is ready to use.
```

### Transition
"Awesome! Our store is live and indexed. Now let's build the API that actually talks to it"

---

## 1:00–1:20 | API Route (20 min)

### Talking Points

**What the API Route Does (3 min)**
- "This is where the magic happens"
- "The frontend will POST messages to `/api/chat`"
- "We use `streamText` from the AI SDK to:"
  - Send messages to Gemini
  - Enable the fileSearch tool
  - Stream the response back chunk by chunk

**Vercel AI SDK Concepts (5 min)**
- "`streamText()` is the core function"
- "It takes:"
  - `model` - which LLM to use
  - `messages` - the conversation history
  - `tools` - what tools the LLM can call
  - `system` - system prompt
- "It returns a stream we send back to the client"
- "The AI SDK handles all the streaming complexity"

**Writing the Route (10 min)**
- Create `app/api/chat/route.ts`
- Walk through each part:
  - Import `streamText` and `google` provider
  - Parse incoming JSON
  - Configure model and tools
  - Return streaming response

**Testing with curl (2 min)**
- "Let's test it before building the UI"
- Show a curl command
- Point out the streaming chunks coming back

### Code to Write

**Create `app/api/chat/route.ts`:**

```typescript
import { streamText } from 'ai';
import { google } from '@ai-sdk/google';
import { STORE_NAME } from '@/lib/store';

export const maxDuration = 30;

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const result = streamText({
      model: google('gemini-2.0-flash-exp'),
      
      system: `You are a helpful assistant that answers questions about MLH (Major League Hacking) documentation.
      
Use the fileSearch tool to find relevant information from the MLH documentation corpus, which includes:
- MLH Hackathon Organizer Guide
- MLH Policies and Code of Conduct
- MLH Hack Days Organizer Guide
- MLH Fellowship information

Always cite your sources when you reference information from the documentation.
If you're not sure about something, say so - don't make up information.
Be friendly, concise, and helpful.`,
      
      messages,
      
      tools: {
        fileSearch: google.tools.fileSearch({
          fileSearchStore: STORE_NAME,
        }),
      },
      
      maxSteps: 5,
    });

    return result.toDataStreamResponse();
    
  } catch (error) {
    console.error('Chat API error:', error);
    return new Response(
      JSON.stringify({ 
        error: 'Failed to process chat request',
        details: error instanceof Error ? error.message : String(error)
      }), 
      { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
```

### Code to Show (Testing)

```bash
# Start the dev server in one terminal
npm run dev

# In another terminal, test the API
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "What is the MLH Code of Conduct?"
      }
    ]
  }'
```

### Common Pitfalls
- **Model name typo:** Make sure it's `gemini-2.0-flash-exp` (check docs for current name)
- **Store name mismatch:** Must match what you created in setup
- **Missing maxDuration:** Vercel has a 10s default timeout - bump it to 30s
- **Forgot to start dev server:** Obvious but happens

### Expected Output

```
0:"..."
0:"The"
0:" MLH"
0:" Code"
0:" of"
0:" Conduct"
...
```

(Streaming chunks of the response)

### Transition
"API is working! Now let's build a beautiful UI to actually use this"

---

## 1:20–1:40 | Chat UI (20 min)

### Talking Points

**The useChat Hook (5 min)**
- "The Vercel AI SDK gives us `useChat()` - a React hook that:"
  - Manages message state
  - Handles form submission
  - Streams responses
  - Updates the UI in real-time
- "It's like... magic. You don't write any streaming code."
- "It calls `/api/chat` automatically and parses the stream"

**Building the UI (12 min)**
- Start with a basic layout: header, messages, input
- Add `useChat()` hook
- Render messages
- Style with Tailwind
- Add example questions for better UX

**Citations Component (3 min)**
- "Citations come from the fileSearch tool results"
- "We'll make them expandable so they don't clutter the UI"
- Quick component to show/hide citation text

### Code to Write

**Create `components/citation.tsx`:**

```typescript
'use client';

import { useState } from 'react';

interface CitationProps {
  text: string;
  source?: string;
  index: number;
}

export function Citation({ text, source, index }: CitationProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="my-2 border border-gray-300 dark:border-gray-700 rounded-lg overflow-hidden">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-2 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors flex items-center justify-between text-left"
      >
        <span className="font-medium text-sm">
          📚 Citation {index + 1}
          {source && (
            <span className="ml-2 text-xs text-gray-600 dark:text-gray-400">
              ({source})
            </span>
          )}
        </span>
        <svg
          className={`w-4 h-4 transition-transform ${
            isExpanded ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      
      {isExpanded && (
        <div className="px-4 py-3 bg-white dark:bg-gray-900 text-sm">
          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
            {text}
          </p>
        </div>
      )}
    </div>
  );
}
```

**Create `components/chat-message.tsx`:**

```typescript
'use client';

import { Message } from 'ai';
import { Citation } from './citation';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  const citations = message.toolInvocations?.flatMap((invocation) => {
    if (invocation.toolName === 'fileSearch' && invocation.state === 'result') {
      const result = invocation.result;
      if (result?.chunks) {
        return result.chunks.map((chunk: any, index: number) => ({
          text: chunk.text || chunk.content,
          source: chunk.source || chunk.uri,
          index,
        }));
      }
    }
    return [];
  }) || [];

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-blue-500 text-white'
            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">
          {message.content}
        </div>

        {!isUser && message.content === '' && (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        )}

        {!isUser && citations.length > 0 && (
          <div className="mt-4 space-y-2">
            {citations.map((citation, index) => (
              <Citation
                key={index}
                text={citation.text}
                source={citation.source}
                index={index}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

**Update `app/page.tsx`:**

```typescript
'use client';

import { useChat } from 'ai/react';
import { ChatMessage } from '@/components/chat-message';

const EXAMPLE_QUESTIONS = [
  "What are the key responsibilities of an MLH hackathon organizer?",
  "What is the MLH Code of Conduct?",
  "How do I run an MLH Hack Day?",
  "What resources does MLH provide for hackathon organizers?",
];

export default function Home() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen bg-white dark:bg-gray-950">
      <header className="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            🤖 MLH Documentation Assistant
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Ask me anything about MLH hackathons, policies, and resources
          </p>
        </div>
      </header>

      <div className="flex-1 overflow-hidden flex max-w-5xl w-full mx-auto">
        <div className="flex-1 flex flex-col">
          <div className="flex-1 overflow-y-auto px-6 py-6 scrollbar-thin">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center">
                <div className="text-center mb-8">
                  <div className="text-6xl mb-4">👋</div>
                  <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
                    Welcome!
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    Ask me anything about MLH documentation
                  </p>
                </div>

                <div className="w-full max-w-2xl">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    Try asking:
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {EXAMPLE_QUESTIONS.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => {
                          const syntheticEvent = {
                            preventDefault: () => {},
                          } as React.FormEvent<HTMLFormElement>;
                          
                          handleInputChange({
                            target: { value: question },
                          } as React.ChangeEvent<HTMLInputElement>);
                          
                          setTimeout(() => handleSubmit(syntheticEvent), 0);
                        }}
                        className="text-left p-4 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors border border-gray-200 dark:border-gray-700"
                      >
                        <p className="text-sm text-gray-700 dark:text-gray-300">
                          {question}
                        </p>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                
                {isLoading && messages[messages.length - 1]?.role === 'user' && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-3">
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {error && (
              <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p className="text-sm text-red-800 dark:text-red-200">
                  ❌ Error: {error.message}
                </p>
              </div>
            )}
          </div>

          <div className="border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4">
            <form onSubmit={handleSubmit} className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={handleInputChange}
                placeholder="Ask a question..."
                disabled={isLoading}
                className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### Common Pitfalls
- **Dark mode not working:** Make sure `globals.css` has the dark mode variables
- **Messages not updating:** Check that you're using `'use client'` directive
- **Citations not showing:** Tool invocations need to be in `result` state
- **Styling looks off:** Double-check Tailwind is configured correctly

### Expected Output
- Clean chat interface
- Messages appear as you type
- Streaming responses update in real-time
- Citations expand/collapse
- Example questions are clickable

### Transition
"Look at that! We have a fully working RAG assistant. Now let's deploy it so you can share it"

---

## 1:40–1:50 | Deploy & Demo (10 min)

### Talking Points

**Why Vercel (2 min)**
- "Vercel is the company behind Next.js"
- "Deployment is literally one command"
- "Free tier is generous - perfect for hackathon projects"

**Deploying Live (5 min)**
- Install Vercel CLI
- Run `vercel deploy --prod`
- Add environment variables in dashboard
- Show the live URL

**Demo Time (3 min)**
- Open the deployed URL
- Ask a few questions live
- Show citations
- Invite chat to try it

**Swapping Docs (if time)**
- "Want to use your own docs?"
- Change the URLs in `lib/store.ts`
- Run setup script again
- That's it!

### Code to Write

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel deploy --prod

# Follow prompts:
# - Link to Vercel account
# - Select project settings
# - Deploy!
```

**Add environment variables in Vercel dashboard:**
1. Go to project settings
2. Environment Variables
3. Add `GOOGLE_API_KEY` and `FILE_SEARCH_STORE_NAME`
4. Redeploy if needed

### Common Pitfalls
- **Forgot env vars:** App will error without them
- **Build fails:** Check build logs - usually missing dependencies
- **Cold starts:** First request might be slow on free tier

### Expected Output
- Live URL: `https://mlh-rag-assistant.vercel.app`
- App works exactly like localhost
- Shareable link you can send to anyone

### Transition
"And that's it! You built and deployed a RAG app in under 2 hours. Let's wrap up"

---

## 1:50–2:00 | Wrap Up (10 min)

### Talking Points

**What We Built (3 min)**
- "In 2 hours, we:"
  - ✅ Created a Next.js app with Tailwind
  - ✅ Set up Gemini File Search for RAG
  - ✅ Built a streaming chat API with the Vercel AI SDK
  - ✅ Created a polished UI with citations
  - ✅ Deployed to production
- "This is a real, production-ready app you can show in interviews"

**Key Takeaways (3 min)**
- "Three big ideas:"
  1. **RAG makes LLMs useful** - No more hallucinations about your docs
  2. **File Search is RAG made easy** - No vector DB, no embeddings, just upload
  3. **AI SDK is the glue** - Streaming, tools, and hooks all in one package

**Next Steps (2 min)**
- "For your hackathon project:"
  - Fork this repo
  - Swap in your own documentation
  - Customize the UI and branding
  - Deploy and submit!
- "Other ideas:"
  - Add voice input/output
  - Support image uploads
  - Multi-language docs
  - Export conversations as PDF

**Resources (1 min)**
- "All the code is on GitHub: [repo link]"
- "Docs:"
  - ai-sdk.dev
  - ai.google.dev/gemini-api/docs/file-search
  - nextjs.org/docs
- "Questions? Drop them in chat or Discord"

**Q&A (1 min)**
- Answer 2-3 quick questions
- "For longer questions, I'll stick around after the stream"

### Code to Show
None - just talking

### Common Pitfalls
None - just don't go over time!

### Expected Output
- Audience feels accomplished
- Clear next steps
- Link to repo
- Open invitation for questions

---

## Post-Stream

- **Save the recording** - edit and upload to YouTube
- **Pin the repo link** in chat and Discord
- **Collect feedback** - what worked, what didn't
- **Answer questions** - stick around for 15-30 min
- **Share highlights** - post clips on Twitter/LinkedIn

---

## Emergency Backup Plans

### If setup-store.ts fails live
- Have a pre-created store ready to go
- Just update the env var and continue
- Explain: "I'll debug this later, let's move on"

### If deployment hangs
- Show the localhost version instead
- Walk through Vercel dashboard manually
- "You can deploy async after the stream"

### If API rate limit hit
- Switch to a backup API key
- Reduce requests (skip example questions)
- Add delays between calls

### If completely stuck
- Switch to the finished code in the repo
- "Let's look at how this works in the final version"
- Keep momentum - don't get stuck debugging for 10 minutes

---

## Final Checklist

- [ ] All code tested end-to-end
- [ ] API keys valid and working
- [ ] Finished demo is running
- [ ] Backup plans in place
- [ ] Screen share tested
- [ ] Audio tested
- [ ] Water nearby
- [ ] Energy high!

**You got this! 🚀**
