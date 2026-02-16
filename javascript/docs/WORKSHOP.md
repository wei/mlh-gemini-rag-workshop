# Build a RAG-Powered Documentation Assistant with Next.js + Vercel AI SDK

**Level:** Intermediate  
**Time:** 2 hours  
**Stack:** Next.js 15, Vercel AI SDK, Gemini File Search, TypeScript, Tailwind CSS

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [What You'll Learn](#what-youll-learn)
4. [Understanding RAG](#understanding-rag)
5. [Architecture Overview](#architecture-overview)
6. [Part 1: Project Setup](#part-1-project-setup)
7. [Part 2: Creating the FileSearchStore](#part-2-creating-the-filesearchstore)
8. [Part 3: Building the Chat API](#part-3-building-the-chat-api)
9. [Part 4: Creating the UI](#part-4-creating-the-ui)
10. [Part 5: Deploying to Vercel](#part-5-deploying-to-vercel)
11. [Troubleshooting](#troubleshooting)
12. [Next Steps](#next-steps)

---

## Introduction

In this workshop, you'll build a **RAG-powered documentation assistant** that can answer questions about MLH (Major League Hacking) documentation with accurate, cited responses.

**What makes this special?**

- 🔍 **No hallucinations** - Answers are grounded in real documentation
- 📚 **Automatic citations** - See exactly where information comes from
- 🚀 **Production-ready** - Deploy to Vercel with one command
- ⚡ **Real-time streaming** - Responses appear as they're generated

By the end, you'll have a working app you can customize for any documentation corpus.

---

## Prerequisites

### Required

- **Node.js 18+** and npm
  ```bash
  node --version  # Should be 18 or higher
  ```

- **Google AI Studio API Key**
  - Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
  - Click "Create API Key"
  - Save it somewhere safe

### Helpful (but not required)

- Basic React knowledge
- Familiarity with Next.js
- Understanding of REST APIs

---

## What You'll Learn

- ✅ What RAG (Retrieval-Augmented Generation) is and why it matters
- ✅ How to use Gemini File Search for document retrieval
- ✅ Building streaming chat APIs with the Vercel AI SDK
- ✅ Using the `useChat()` hook for real-time UIs
- ✅ Deploying full-stack Next.js apps to Vercel

---

## Understanding RAG

### The Problem

Large language models (LLMs) like GPT-4 and Gemini are amazing, but they have a critical limitation: **they don't know about your private documentation**.

If you ask Gemini about your company's internal wiki or a new product you just launched, it will either:
- Make up an answer (hallucinate)
- Say "I don't know"

### The Solution: RAG

**Retrieval-Augmented Generation (RAG)** solves this by combining retrieval and generation:

```
User Question
     ↓
1. RETRIEVE: Search your docs for relevant information
     ↓
2. AUGMENT: Add that information to the LLM's context
     ↓
3. GENERATE: LLM produces an accurate, grounded answer
```

### Traditional RAG Pipeline

Normally, you'd need to build:

1. **Embedding Model** - Convert text to vectors (OpenAI, Cohere)
2. **Vector Database** - Store and search vectors (Pinecone, Weaviate)
3. **Chunking Strategy** - Split docs into optimal sizes
4. **Retrieval Logic** - Query the vector DB
5. **Prompt Engineering** - Format context for the LLM

That's a lot of moving parts!

### Gemini File Search: RAG Made Easy

**Gemini File Search** handles all of that for you:

- ✅ Automatic embeddings
- ✅ Managed vector store
- ✅ Smart chunking
- ✅ Integrated with Gemini models
- ✅ Built-in citation tracking

**You just upload files. Google handles the rest.**

---

## Architecture Overview

Here's what we're building:

```
┌─────────────────────────────────────────────────────────────┐
│  Browser (React)                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  useChat() hook                                       │  │
│  │  - Manages messages state                            │  │
│  │  - Handles form submission                           │  │
│  │  - Streams responses from API                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    POST /api/chat
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Next.js API Route                                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  streamText()                                         │  │
│  │  - model: google('gemini-2.0-flash')                 │  │
│  │  - tools: { fileSearch }                             │  │
│  │  - Streams response chunks back                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Gemini API                                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FileSearchStore                                      │  │
│  │  - MLH Hackathon Organizer Guide                     │  │
│  │  - MLH Policies                                       │  │
│  │  - MLH Code of Conduct                               │  │
│  │  - MLH Hack Days Guide                               │  │
│  │  - MLH Fellowship FAQ                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Frontend** (`app/page.tsx`)
   - Uses `useChat()` hook from `ai/react`
   - Manages chat state automatically
   - Streams responses in real-time

2. **API Route** (`app/api/chat/route.ts`)
   - Uses `streamText()` from `ai`
   - Configures Gemini model with fileSearch tool
   - Returns streaming response

3. **FileSearchStore** (created by setup script)
   - Stores MLH documentation
   - Indexed by Google AI
   - Queried automatically via fileSearch tool

---

## Part 1: Project Setup

### Step 1: Create a New Next.js Project

```bash
npx create-next-app@latest mlh-rag-assistant
```

When prompted, choose:

```
✔ Would you like to use TypeScript? … Yes
✔ Would you like to use ESLint? … Yes
✔ Would you like to use Tailwind CSS? … Yes
✔ Would you like your code inside a `src/` directory? … No
✔ Would you like to use App Router? … Yes
✔ Would you like to use Turbopack for `next dev`? … No
✔ Would you like to customize the import alias? … No
```

Navigate into the project:

```bash
cd mlh-rag-assistant
```

### Step 2: Install Dependencies

Install the Vercel AI SDK and Google provider:

```bash
npm install ai @ai-sdk/google @google/generative-ai
```

Install tsx for running TypeScript scripts:

```bash
npm install -D tsx
```

**What we installed:**

- `ai` - Vercel AI SDK core (streamText, useChat)
- `@ai-sdk/google` - Google provider for AI SDK
- `@google/generative-ai` - Google's official SDK (for store setup)
- `tsx` - TypeScript executor (like ts-node but faster)

### Step 3: Set Up Environment Variables

Create a `.env.local` file in the project root:

```bash
touch .env.local
```

Add your configuration:

```env
# Get your API key from https://aistudio.google.com/apikey
GOOGLE_API_KEY=your_api_key_here

# The name of the FileSearchStore (we'll create this next)
FILE_SEARCH_STORE_NAME=mlh-docs-store
```

**Important:** Replace `your_api_key_here` with your actual Google AI API key.

### Step 4: Create Store Configuration

Create a `lib` folder and add `store.ts`:

```bash
mkdir lib
touch lib/store.ts
```

**`lib/store.ts`:**

```typescript
/**
 * Shared FileSearchStore configuration
 */

// Get store name from environment variable
export const STORE_NAME = process.env.FILE_SEARCH_STORE_NAME || 'mlh-docs-store';

// MLH documentation URLs (raw markdown from GitHub)
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

This file defines:
- The name of our FileSearchStore
- The documents we'll upload

### Step 5: Add Setup Script to package.json

Open `package.json` and add a new script:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "setup-store": "tsx scripts/setup-store.ts"
  }
}
```

### ✅ Checkpoint

You should now have:

```
mlh-rag-assistant/
├── app/
├── lib/
│   └── store.ts
├── node_modules/
├── public/
├── .env.local
├── .gitignore
├── next.config.ts
├── package.json
├── README.md
├── tailwind.config.ts
└── tsconfig.json
```

**Test it:**

```bash
npm run dev
```

You should see:

```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
```

Open [http://localhost:3000](http://localhost:3000) to see the default Next.js page.

---

## Part 2: Creating the FileSearchStore

Now we'll write a script that:
1. Creates a FileSearchStore in Google AI
2. Downloads MLH documentation from GitHub
3. Uploads the docs to the store
4. Waits for indexing to complete
5. Tests the store with a query

### Step 1: Create the Scripts Directory

```bash
mkdir scripts
touch scripts/setup-store.ts
```

### Step 2: Write the Setup Script

**`scripts/setup-store.ts`:**

```typescript
/**
 * Setup script: Create FileSearchStore and upload MLH documentation
 * 
 * This script:
 * 1. Creates a FileSearchStore in Google AI
 * 2. Downloads MLH docs from GitHub
 * 3. Uploads them to the store
 * 4. Polls until indexing is complete
 * 
 * Run: npm run setup-store
 */

import { GoogleGenAI } from '@google/generative-ai';
import { STORE_NAME, MLH_DOCS } from '../lib/store';
import * as fs from 'fs';
import * as path from 'path';

const API_KEY = process.env.GOOGLE_API_KEY;

if (!API_KEY) {
  console.error('❌ GOOGLE_API_KEY environment variable is required');
  console.error('Get your key from https://aistudio.google.com/apikey');
  process.exit(1);
}

const genai = new GoogleGenAI(API_KEY);

/**
 * Download a file from URL to a local temp path
 */
async function downloadFile(url: string, filename: string): Promise<string> {
  console.log(`  📥 Downloading ${filename}...`);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to download ${url}: ${response.statusText}`);
  }
  
  const content = await response.text();
  const tmpDir = path.join(process.cwd(), 'tmp');
  
  // Create tmp directory if it doesn't exist
  if (!fs.existsSync(tmpDir)) {
    fs.mkdirSync(tmpDir, { recursive: true });
  }
  
  const filepath = path.join(tmpDir, filename);
  fs.writeFileSync(filepath, content, 'utf-8');
  console.log(`  ✅ Saved to ${filepath}`);
  return filepath;
}

/**
 * Create a FileSearchStore
 */
async function createStore(name: string) {
  console.log(`\n🏗️  Creating FileSearchStore: ${name}`);
  
  try {
    // Check if store already exists
    const existingStore = await genai.fileSearchStores.get(name);
    console.log(`✅ Store "${name}" already exists`);
    return existingStore;
  } catch (error) {
    // Store doesn't exist, create it
    console.log(`  Creating new store...`);
    const store = await genai.fileSearchStores.create({
      displayName: name,
    });
    console.log(`✅ Store created: ${store.name}`);
    return store;
  }
}

/**
 * Upload files to the store
 */
async function uploadFiles(storeName: string, filepaths: string[]) {
  console.log(`\n📤 Uploading ${filepaths.length} files...`);
  
  const uploadedFiles = [];
  
  for (const filepath of filepaths) {
    const filename = path.basename(filepath);
    console.log(`  Uploading ${filename}...`);
    
    const fileContent = fs.readFileSync(filepath);
    
    // Upload file to Google AI
    const file = await genai.files.upload({
      file: {
        data: fileContent,
        mimeType: 'text/markdown',
      },
      displayName: filename,
    });
    
    console.log(`  ✅ Uploaded: ${file.name}`);
    
    // Add file to store
    await genai.fileSearchStores.addFile(storeName, file.name);
    console.log(`  ➕ Added to store`);
    
    uploadedFiles.push(file.name);
  }
  
  return uploadedFiles;
}

/**
 * Poll store state until indexing is complete
 */
async function waitForIndexing(storeName: string) {
  console.log(`\n⏳ Waiting for indexing to complete...`);
  
  let attempts = 0;
  const maxAttempts = 60; // 5 minutes max
  
  while (attempts < maxAttempts) {
    const store = await genai.fileSearchStores.get(storeName);
    
    if (store.state === 'ACTIVE') {
      console.log(`✅ Indexing complete! Store is ACTIVE`);
      return;
    }
    
    console.log(`  State: ${store.state} (attempt ${attempts + 1}/${maxAttempts})`);
    
    // Wait 5 seconds before next check
    await new Promise(resolve => setTimeout(resolve, 5000));
    attempts++;
  }
  
  throw new Error('Indexing timed out after 5 minutes');
}

/**
 * Test the store with a sample query
 */
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
  
  // Show citations if available
  if (response.candidates?.[0]?.groundingMetadata?.groundingChunks) {
    const chunks = response.candidates[0].groundingMetadata.groundingChunks;
    console.log(`\n📚 Citations: ${chunks.length} source(s)`);
  }
}

/**
 * Main setup flow
 */
async function main() {
  console.log('🚀 MLH RAG Store Setup\n');
  console.log(`Store name: ${STORE_NAME}`);
  console.log(`Documents: ${MLH_DOCS.length}\n`);
  
  try {
    // Step 1: Create store
    const store = await createStore(STORE_NAME);
    
    // Step 2: Download docs
    console.log(`\n📥 Downloading MLH documentation...`);
    const filepaths: string[] = [];
    
    for (const doc of MLH_DOCS) {
      const filepath = await downloadFile(doc.url, `${doc.name}.md`);
      filepaths.push(filepath);
    }
    
    // Step 3: Upload to store
    await uploadFiles(store.name, filepaths);
    
    // Step 4: Wait for indexing
    await waitForIndexing(store.name);
    
    // Step 5: Test with a query
    await testQuery(store.name);
    
    // Cleanup temp files
    console.log(`\n🧹 Cleaning up temp files...`);
    for (const filepath of filepaths) {
      fs.unlinkSync(filepath);
    }
    fs.rmdirSync(path.join(process.cwd(), 'tmp'));
    
    console.log(`\n✨ Setup complete! Your store is ready to use.`);
    console.log(`\nNext steps:`);
    console.log(`  1. Make sure .env.local has your GOOGLE_API_KEY`);
    console.log(`  2. Run: npm run dev`);
    
  } catch (error) {
    console.error(`\n❌ Setup failed:`, error);
    process.exit(1);
  }
}

main();
```

### Step 3: Run the Setup Script

```bash
npm run setup-store
```

**Expected Output:**

```
🚀 MLH RAG Store Setup

Store name: mlh-docs-store
Documents: 5

🏗️  Creating FileSearchStore: mlh-docs-store
  Creating new store...
✅ Store created: projects/xxx/fileSearchStores/mlh-docs-store

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
MLH hackathon organizers have several key responsibilities, including...
[Full response]

📚 Citations: 3 source(s)

🧹 Cleaning up temp files...

✨ Setup complete! Your store is ready to use.

Next steps:
  1. Make sure .env.local has your GOOGLE_API_KEY
  2. Run: npm run dev
```

This process takes about 1-2 minutes.

### ✅ Checkpoint

- Your FileSearchStore is created and indexed
- MLH docs are uploaded and searchable
- The store is in ACTIVE state
- Test query returned a grounded response

---

## Part 3: Building the Chat API

Now we'll create the API route that handles chat requests using the Vercel AI SDK.

### Step 1: Create the API Route

```bash
mkdir -p app/api/chat
touch app/api/chat/route.ts
```

### Step 2: Write the API Route

**`app/api/chat/route.ts`:**

```typescript
/**
 * Chat API Route
 * 
 * Uses Vercel AI SDK with:
 * - streamText for streaming responses
 * - google('gemini-2.0-flash') model
 * - google.tools.fileSearch() for RAG
 */

import { streamText } from 'ai';
import { google } from '@ai-sdk/google';
import { STORE_NAME } from '@/lib/store';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

export async function POST(req: Request) {
  try {
    // Parse incoming messages from the client
    const { messages } = await req.json();

    // Stream the response using Vercel AI SDK
    const result = streamText({
      // Use Gemini 2.0 Flash model via AI SDK Google provider
      model: google('gemini-2.0-flash-exp'),
      
      // System prompt to guide the assistant
      system: `You are a helpful assistant that answers questions about MLH (Major League Hacking) documentation.
      
Use the fileSearch tool to find relevant information from the MLH documentation corpus, which includes:
- MLH Hackathon Organizer Guide
- MLH Policies and Code of Conduct
- MLH Hack Days Organizer Guide
- MLH Fellowship information

Always cite your sources when you reference information from the documentation.
If you're not sure about something, say so - don't make up information.
Be friendly, concise, and helpful.`,
      
      // User messages from the chat
      messages,
      
      // Configure RAG with fileSearch tool
      tools: {
        // The fileSearch tool automatically retrieves relevant docs
        fileSearch: google.tools.fileSearch({
          fileSearchStore: STORE_NAME,
        }),
      },
      
      // Automatically execute tool calls
      maxSteps: 5,
    });

    // Return the streaming response
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

### Understanding the Code

**`streamText()` Parameters:**

- `model` - Which LLM to use (`google('gemini-2.0-flash-exp')`)
- `system` - Instructions for the AI assistant
- `messages` - Conversation history from the client
- `tools` - Tools the AI can use (fileSearch for RAG)
- `maxSteps` - How many tool calls can be chained

**`tools.fileSearch`:**

- Configured with our FileSearchStore name
- AI automatically decides when to use it
- Retrieves relevant chunks from our docs
- Returns results with citations

**`result.toDataStreamResponse()`:**

- Converts the stream to a Response object
- Chunks are sent as they're generated
- Client receives updates in real-time

### Step 3: Test the API

Start the dev server:

```bash
npm run dev
```

Test with curl:

```bash
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

**Expected Output:**

```
0:"..."
0:"The"
0:" MLH"
0:" Code"
0:" of"
0:" Conduct"
...
```

You should see streaming chunks of the response!

### ✅ Checkpoint

- API route is working
- Streaming responses are returned
- fileSearch tool is retrieving documents

---

## Part 4: Creating the UI

Now let's build the chat interface using the Vercel AI SDK's `useChat()` hook.

### Step 1: Create the Citation Component

```bash
mkdir components
touch components/citation.tsx
```

**`components/citation.tsx`:**

```typescript
/**
 * Citation component - displays expandable source citations
 */

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

### Step 2: Create the ChatMessage Component

```bash
touch components/chat-message.tsx
```

**`components/chat-message.tsx`:**

```typescript
/**
 * ChatMessage component - displays a single message with citations
 */

'use client';

import { Message } from 'ai';
import { Citation } from './citation';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  // Extract citations from tool invocations
  const citations = message.toolInvocations?.flatMap((invocation) => {
    if (invocation.toolName === 'fileSearch' && invocation.state === 'result') {
      // Parse fileSearch results for citations
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
        {/* Message content */}
        <div className="whitespace-pre-wrap break-words">
          {message.content}
        </div>

        {/* Loading indicator for assistant */}
        {!isUser && message.content === '' && (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        )}

        {/* Citations */}
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

### Step 3: Update the Main Page

Replace `app/page.tsx` with:

```typescript
/**
 * Main Chat Page
 * 
 * Uses Vercel AI SDK's useChat hook for:
 * - Managing chat state
 * - Streaming responses
 * - Form handling
 */

'use client';

import { useChat } from 'ai/react';
import { ChatMessage } from '@/components/chat-message';

// Example questions to help users get started
const EXAMPLE_QUESTIONS = [
  "What are the key responsibilities of an MLH hackathon organizer?",
  "What is the MLH Code of Conduct?",
  "How do I run an MLH Hack Day?",
  "What resources does MLH provide for hackathon organizers?",
];

export default function Home() {
  // useChat hook manages all chat state and API communication
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen bg-white dark:bg-gray-950">
      {/* Header */}
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

      {/* Main content area */}
      <div className="flex-1 overflow-hidden flex max-w-5xl w-full mx-auto">
        {/* Chat messages */}
        <div className="flex-1 flex flex-col">
          {/* Messages container */}
          <div className="flex-1 overflow-y-auto px-6 py-6 scrollbar-thin">
            {messages.length === 0 ? (
              // Welcome screen with example questions
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

                {/* Example questions */}
                <div className="w-full max-w-2xl">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    Try asking:
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {EXAMPLE_QUESTIONS.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => {
                          // Create a synthetic form event
                          const syntheticEvent = {
                            preventDefault: () => {},
                          } as React.FormEvent<HTMLFormElement>;
                          
                          // Set the input value and submit
                          handleInputChange({
                            target: { value: question },
                          } as React.ChangeEvent<HTMLInputElement>);
                          
                          // Submit on next tick to ensure input is set
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
              // Message list
              <div className="space-y-4">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                
                {/* Loading indicator */}
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

            {/* Error display */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p className="text-sm text-red-800 dark:text-red-200">
                  ❌ Error: {error.message}
                </p>
              </div>
            )}
          </div>

          {/* Input form */}
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

### Step 4: Update Global Styles

Replace `app/globals.css` with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #ffffff;
  --foreground: #171717;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: Arial, Helvetica, sans-serif;
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}

/* Custom scrollbar */
.scrollbar-thin::-webkit-scrollbar {
  width: 8px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #555;
}
```

### Step 5: Test the UI

Make sure the dev server is running:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

Try:
1. Click an example question
2. Watch the response stream in real-time
3. Expand citations to see source text
4. Ask your own questions

### ✅ Checkpoint

You should have:
- A clean, modern chat interface
- Streaming responses appearing word-by-word
- Expandable citations showing source text
- Example questions for easy testing

---

## Part 5: Deploying to Vercel

Let's deploy your app so you can share it with the world!

### Step 1: Install Vercel CLI

```bash
npm i -g vercel
```

### Step 2: Deploy

```bash
vercel deploy --prod
```

Follow the prompts:

```
? Set up and deploy "~/mlh-rag-assistant"? yes
? Which scope do you want to deploy to? [Your username]
? Link to existing project? no
? What's your project's name? mlh-rag-assistant
? In which directory is your code located? ./
```

Vercel will:
- Build your Next.js app
- Deploy it to their CDN
- Give you a live URL

### Step 3: Add Environment Variables

After deployment, add your environment variables:

1. Go to [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Click your project
3. Go to **Settings** → **Environment Variables**
4. Add:
   - `GOOGLE_API_KEY` = your API key
   - `FILE_SEARCH_STORE_NAME` = `mlh-docs-store`
5. Click **Save**

### Step 4: Redeploy

```bash
vercel deploy --prod
```

This time it will use your environment variables.

### Step 5: Test Your Live App

Open the deployment URL (something like `https://mlh-rag-assistant.vercel.app`)

Try asking questions - it should work exactly like localhost!

### ✅ Checkpoint

- Your app is live on the internet
- You have a shareable URL
- It works just like your local version

---

## Troubleshooting

### "Store not found" Error

**Problem:** The API can't find your FileSearchStore.

**Solution:**
1. Check that you ran `npm run setup-store` successfully
2. Verify the store name in `.env.local` matches what you created
3. Make sure `.env.local` is loaded (restart the dev server)

### API Key Errors

**Problem:** "Invalid API key" or "API key not found"

**Solution:**
1. Get your key from [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Make sure it's in `.env.local` as `GOOGLE_API_KEY=your_key`
3. Restart the dev server after updating `.env.local`
4. Don't commit `.env.local` to git - it should be in `.gitignore`

### Indexing Takes Too Long

**Problem:** Setup script waits forever for indexing.

**Solution:**
1. Check your internet connection
2. Verify API key has access to Gemini File Search
3. Wait up to 5 minutes - indexing can be slow
4. If it times out, run the script again (it will reuse the existing store)

### No Citations Showing

**Problem:** Responses don't include citations.

**Solution:**
1. Check that the store is in ACTIVE state (run setup-store again to verify)
2. Verify `FILE_SEARCH_STORE_NAME` matches in `.env.local`
3. Look for errors in browser console
4. Make sure the model is actually using the fileSearch tool (check API logs)

### Build Fails on Vercel

**Problem:** Deployment fails with build errors.

**Solution:**
1. Run `npm run build` locally to check for errors
2. Make sure all dependencies are in `package.json`
3. Check that TypeScript has no errors
4. Look at Vercel build logs for specific error messages

### Dark Mode Issues

**Problem:** Dark mode looks broken or doesn't work.

**Solution:**
1. Check that `globals.css` has dark mode styles
2. Verify Tailwind config includes dark mode classes
3. Make sure components use `dark:` prefixed classes
4. Try toggling dark mode in your OS settings

---

## Next Steps

Congratulations! You've built a fully functional RAG-powered documentation assistant. Here's what you can do next:

### 🎨 Customize for Your Docs

1. Edit `lib/store.ts` to point to your documentation URLs
2. Update example questions in `app/page.tsx`
3. Modify the system prompt in `app/api/chat/route.ts`
4. Run `npm run setup-store` to index your new docs

### ✨ Add Features

- **Voice input/output** - Use Web Speech API or ElevenLabs
- **Image support** - Upload images with questions
- **Export conversations** - Save as PDF or Markdown
- **Multi-language** - Support docs in different languages
- **Authentication** - Add user accounts with Clerk or Auth.js
- **Analytics** - Track popular questions and usage

### 🚀 Advanced Topics

- **Custom chunking strategies** - Optimize for your document structure
- **Hybrid search** - Combine semantic and keyword search
- **Feedback loops** - Let users rate answers to improve quality
- **Fine-tuning** - Train a custom model on your domain
- **Cost optimization** - Cache responses, reduce token usage

### 📚 Learn More

- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Gemini File Search Guide](https://ai.google.dev/gemini-api/docs/file-search)
- [Next.js App Router Docs](https://nextjs.org/docs/app)
- [RAG Best Practices](https://www.llamaindex.ai/blog/a-guide-to-rag-best-practices)

---

## Challenge: Build Your Own

**Task:** Create a RAG assistant for a different use case.

Ideas:
- Company policy Q&A
- Product documentation helper
- Legal document assistant
- Academic paper explorer
- Recipe recommendation bot

**Requirements:**
- At least 3 documents in your store
- Custom system prompt
- Styled UI with your branding
- Deployed to Vercel

Share your project in the MLH Discord!

---

## Resources

### Documentation

- [Vercel AI SDK](https://sdk.vercel.ai/docs)
- [Google AI SDK](https://ai.google.dev/gemini-api/docs)
- [Next.js](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Example Code

- [Finished app](../finished/)
- [Stream plan](../STREAM_PLAN.md)
- [GitHub repo](https://github.com/wei/mlh-gemini-rag-workshop)

### Community

- [MLH Discord](https://discord.mlh.io/)
- [Vercel Discord](https://vercel.com/discord)
- [Next.js Discussions](https://github.com/vercel/next.js/discussions)

---

**Happy building! 🚀**
