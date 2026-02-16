# 2-Hour Stream Plan: Build a RAG-Powered Doc Assistant

**Target Audience:** Developers/students learning RAG with Python + Streamlit + Gemini File Search  
**Duration:** 2 hours  
**Format:** Live coding workshop  
**Demo Corpus:** MLH documentation (hackathon organizer guide, policies, code of conduct, hack days guide)

---

## Pre-Stream Checklist

- [ ] Tested all code in a fresh Python environment
- [ ] API key ready (not shown on screen)
- [ ] Terminal font size readable (18pt+)
- [ ] Code editor ready with syntax highlighting
- [ ] Browser tabs: AI Studio, GitHub repos, Gemini docs
- [ ] Backup: finished code ready in case of catastrophic failure
- [ ] OBS scenes: code editor, browser, terminal, webcam
- [ ] Test stream audio/video

---

## 🎬 Segment 1: Intro & Context (0:00–0:10)

**Goal:** Welcome, show the finished demo, explain what we're building

### Talking Points

```
👋 Welcome to MLH Global Hack Week!

I'm [name] and today we're building a RAG-powered documentation assistant.

By the end of this stream, you'll have:
- A working chatbot that answers questions about MLH docs
- Understanding of how RAG works under the hood
- Code you can adapt to ANY documentation

This isn't theoretical — we're building something you can deploy today.
```

### Show Finished Demo (3 min)

**Run the finished app:**

```bash
cd finished/
streamlit run app.py
```

**Ask these questions on stream:**
1. "How do I get reimbursed for a Hack Day?"
   - Point out the answer
   - Show citations
   - Click to expand and see the source text

2. "What are MLH's code of conduct policies?"
   - Show different documents being cited
   - Emphasize: NOT making this up, pulled from actual docs

3. "What's the capital of France?" (trick question)
   - Show it either refuses or says "not in docs"
   - This is the power of RAG: grounded responses

**Say:**
```
See those citations? That's proof the model isn't hallucinating.
Every answer comes from real documents we uploaded.

Now let's build this from scratch.
```

### What We're Building (2 min)

**Architecture diagram (draw or show slide):**

```
User Question
     ↓
[ Streamlit UI ]
     ↓
[ Gemini API ] → [ File Search Tool ] → [ Vector Store ]
     ↓                                        ↑
  Response                            [ MLH Docs ]
```

**Say:**
```
Three main steps:
1. Setup (one-time): Upload docs to create a vector store
2. Query: User asks a question
3. RAG: Retrieve relevant chunks + generate answer

We'll code all three pieces.
```

### Tech Stack (2 min)

**Show on screen:**

| Component | Technology | Why |
|-----------|------------|-----|
| Backend | Python + `google-genai` SDK | Official Gemini SDK |
| RAG | Gemini File Search | Automatic chunking, embeddings, retrieval |
| UI | Streamlit | Chat interface in 10 lines |
| Docs | MLH markdown files | Real-world documentation |

**Say:**
```
No need for separate vector DB (Pinecone, Weaviate, etc.)
No manual chunking or embedding code
Gemini File Search handles it all.

This is the fastest way to build production RAG in 2026.
```

### Transition (1 min)

```
Before we code, let's understand WHY we need RAG.
```

**Common Pitfalls:**
- Don't go over time — intro sets the energy
- Test the demo beforehand (don't debug live here)
- Have backup screen recording if demo fails

---

## 📚 Segment 2: RAG Deep Dive (0:10–0:25)

**Goal:** Explain RAG concepts, why LLMs hallucinate, what Gemini File Search automates

### Why LLMs Hallucinate (3 min)

**Live demo with ChatGPT or Gemini (in browser):**

**Ask:** "What are the requirements for an MLH Hack Day?"

**Show:**
- Model generates plausible but WRONG answer
- Sounds confident
- No way to verify

**Say:**
```
The model's training data has a cutoff date.
It doesn't know about YOUR specific documentation.
So it makes up plausible-sounding answers.

This is called "hallucination" and it's a HUGE problem
for using LLMs with internal docs, policies, etc.

RAG solves this.
```

### What is RAG? (5 min)

**Explain step-by-step (draw/animate on screen):**

#### Traditional LLM:
```
User: "How do I get reimbursed?"
  ↓
LLM: [generates from memory] → "You need to submit Form X..." (WRONG)
```

#### RAG Pipeline:
```
1. INDEXING (one-time setup):
   Docs → Chunks → Embeddings → Vector Database
   
2. RETRIEVAL (per query):
   User question → Embedding → Search vector DB → Top-K chunks
   
3. GENERATION:
   Chunks + Question → LLM → Grounded answer + citations
```

**Detailed walkthrough:**

**1. Chunking:**
```
Why: Documents are too long for LLM context windows
How: Split into ~500-1000 token chunks with overlap

Example:
Doc: "MLH Hack Days are student-led events..."
↓
Chunk 1: "MLH Hack Days are student-led events that..."
Chunk 2: "...that bring together students to learn..."
```

**2. Embeddings:**
```
Why: Need numerical representation for semantic search
How: Transform text → high-dimensional vector

"MLH Hack Day" → [0.23, -0.45, 0.67, ..., 0.12]  (768 dims)

Similar meaning = vectors close together in space
```

**3. Vector Store:**
```
Why: Fast similarity search across millions of chunks
How: Specialized database (HNSW, IVF algorithms)

Think: "Google for semantic meaning"
```

**4. Retrieval:**
```
User: "How do I get reimbursed?"
  ↓
Embed question: [0.18, -0.52, 0.71, ...]
  ↓
Search vector DB for closest chunk vectors
  ↓
Return Top-K (usually 5-10) most relevant chunks
```

**5. Generation:**
```
Prompt to LLM:
  "Use these documents to answer the question:
   
   [Chunk 1]: ...reimbursement requires submission of receipts...
   [Chunk 2]: ...approved expenses include venue costs...
   [Chunk 3]: ...reimbursement processed within 30 days...
   
   Question: How do I get reimbursed?"
   
LLM generates grounded answer, cites sources.
```

### What Gemini File Search Automates (3 min)

**Show the comparison table:**

| Task | Manual RAG | Gemini File Search |
|------|-----------|-------------------|
| Chunking strategy | You write code | ✅ Automatic |
| Embedding model | Manage separately | ✅ Built-in |
| Vector database | Deploy & maintain | ✅ Hosted |
| Retrieval logic | Custom implementation | ✅ API call |
| Citation extraction | Parse metadata | ✅ Structured response |

**Say:**
```
Normally you'd need:
- LangChain or LlamaIndex for chunking
- Pinecone, Weaviate, or Chroma for vector DB
- Separate embedding API calls
- Complex retrieval logic

With Gemini File Search:
- Upload files
- Query
- Done

This is HUGE for rapid prototyping and production.
```

### RAG Limitations (2 min)

**Be honest about trade-offs:**

```
RAG is powerful but not magic:

❌ Won't work if info isn't in the docs
❌ Quality depends on chunking (but Gemini handles this)
❌ Can retrieve irrelevant chunks (low quality = bad answers)
❌ Adds latency (retrieval step + longer context)
✅ But eliminates hallucination for in-scope questions
✅ Always provides sources (verifiable)
✅ Easy to update (just add new docs)
```

### Transition (2 min)

```
Alright, theory is done. Let's code!

We'll build in 3 stages:
1. Setup: Create vector store, upload docs
2. Query: Test from command line
3. UI: Build Streamlit chat interface

Let's go!
```

**Common Pitfalls:**
- Don't rush explanations — this is the foundation
- Use visuals (diagrams, animations)
- Relate to real-world examples (Google search, recommendation engines)
- Answer chat questions but don't derail

---

## 🛠️ Segment 3: Project Setup (0:25–0:40)

**Goal:** Install deps, get API key, prove Gemini works with first API call

### Create Project Directory (2 min)

**Type in terminal (explain each step):**

```bash
mkdir mlh-rag-workshop
cd mlh-rag-workshop

# Check Python version
python --version  # Need 3.10+

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows
```

**Say:**
```
Virtual environments keep dependencies isolated.
Good practice for any Python project.

You'll see (venv) in your terminal now.
```

### Install Dependencies (3 min)

**Create requirements.txt:**

```bash
touch requirements.txt
```

**Type in requirements.txt:**

```
google-genai>=1.0.0
streamlit>=1.30.0
python-dotenv>=1.0.0
requests>=2.31.0
```

**Explain each one:**

```
google-genai:    Official Gemini SDK
streamlit:       Chat UI framework
python-dotenv:   Load API keys from .env
requests:        Download docs from GitHub
```

**Install:**

```bash
pip install -r requirements.txt
```

**Say:**
```
This will take ~30 seconds.
[While waiting, chat with audience about their experience with APIs]
```

### Get API Key (3 min)

**Show in browser:**

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy the key (blur it on stream!)

**Say:**
```
This is YOUR API key — don't share it publicly.
In production, you'd use secret management.

For now, we'll use a .env file (which we'll gitignore).
```

**Create .env file:**

```bash
touch .env
echo ".env" >> .gitignore
```

**Type in .env:**

```bash
GEMINI_API_KEY=your-api-key-here
```

**Replace with actual key** (but blur on screen!)

### First API Call (7 min)

**Create test.py:**

```python
#!/usr/bin/env python3
"""
Test that Gemini API is working.
"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env")
    exit(1)

print("✅ API key loaded")

# Create client
client = genai.Client(api_key=api_key)
print("✅ Client created")

# Test generate_content
print("\n🧪 Testing generate_content...\n")

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Say "Hello from Gemini!" in a friendly way.'
)

print(response.text)
print("\n✅ API is working!")
```

**Run it:**

```bash
python test.py
```

**Expected output:**

```
✅ API key loaded
✅ Client created

🧪 Testing generate_content...

Hello from Gemini! 👋 It's great to connect with you!

✅ API is working!
```

**Explain the code:**

```
1. load_dotenv() reads .env file
2. genai.Client() creates API client
3. generate_content() sends prompt, gets response
4. response.text extracts the string

Simple! Now let's add RAG.
```

### Transition (1 min)

```
We've proven the API works.

Next: Create a vector store and upload MLH docs.
This is the "indexing" phase of RAG.
```

**Common Pitfalls:**
- Have API key ready before stream (don't wait for email verification)
- Blur API key on screen (use OBS filter or code editor blur)
- If rate limited, have backup client
- Windows users: help with venv activation in chat

---

## 🗄️ Segment 4: Build the RAG Pipeline (0:40–1:00)

**Goal:** Create FileSearchStore, upload docs, test first query with citations

### Create setup_store.py (10 min)

**Say:**
```
We need to upload our docs ONCE to create a vector store.
Let's write a script for that.
```

**Create setup_store.py:**

```python
#!/usr/bin/env python3
"""
Setup script to create FileSearchStore and upload MLH docs.
"""

import os
import time
import tempfile
import requests
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# MLH docs to index (raw GitHub URLs)
MLH_DOCS = {
    "hackathon-organizer-guide.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/master/README.md",
    "what-is-mlh.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/master/overview/what-is-mlh.md",
    "hackathon-timeline.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/master/general-information/hackathon-timeline.md",
    "getting-sponsorship.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/master/general-information/getting-sponsorship/README.md",
    "managing-registrations.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/master/general-information/managing-registrations/README.md",
    "judging-and-submissions.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/master/general-information/judging-and-submissions/README.md",
    "mlh-community-values.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/master/overview/mlh-community-values.md",
    "code-of-conduct.md": "https://raw.githubusercontent.com/MLH/mlh-policies/main/code-of-conduct.md",
    "community-values.md": "https://raw.githubusercontent.com/MLH/mlh-policies/main/community-values.md",
    "hack-days-guide.md": "https://raw.githubusercontent.com/MLH/mlh-hack-days-organizer-guide/main/README.md",
}

def download_file(url: str, filename: str, temp_dir: Path) -> Path:
    """Download file from GitHub."""
    print(f"  Downloading {filename}...")
    response = requests.get(url)
    response.raise_for_status()
    
    file_path = temp_dir / filename
    file_path.write_text(response.text, encoding='utf-8')
    return file_path

def main():
    # Initialize client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
    
    client = genai.Client(api_key=api_key)
    
    # Create FileSearchStore
    print("📦 Creating FileSearchStore...")
    store = client.file_search_stores.create(
        config=types.CreateFileSearchStoreConfig(
            display_name="MLH Documentation Store",
        )
    )
    print(f"✅ Created: {store.name}\n")
    
    # Download and upload docs
    print("📥 Uploading documents...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for filename, url in MLH_DOCS.items():
            try:
                # Download
                file_path = download_file(url, filename, temp_path)
                
                # Upload directly to the FileSearchStore
                print(f"  Uploading {filename}...")
                operation = client.file_search_stores.upload_to_file_search_store(
                    file_search_store_name=store.name,
                    file=str(file_path),
                )
                
                # Wait for upload operation to complete
                while not operation.done:
                    time.sleep(2)
                    operation = client.operations.get(operation)
                
                print(f"✅ {filename} uploaded\n")
                
            except Exception as e:
                print(f"❌ Error with {filename}: {e}\n")
    
    # Print instructions
    print("="*60)
    print("🎉 Setup complete!")
    print("="*60)
    print(f"\nStore name: {store.name}")
    print("\nAdd this to your .env file:")
    print(f"FILE_SEARCH_STORE_NAME={store.name}")
    print()

if __name__ == "__main__":
    main()
```

**Explain key parts:**

```
1. MLH_DOCS dict: Maps filename → raw GitHub URL
2. tempfile: Download to temp folder (auto-cleanup)
3. client.file_search_stores.create(): Creates empty store
4. upload_to_file_search_store(): Uploads file directly to store
5. operations.get(): Polls until upload completes
```

**Run it:**

```bash
python setup_store.py
```

**Live output:**

```
📦 Creating FileSearchStore...
✅ Created: fileSearchStores/abc123xyz

📥 Uploading documents...
  Downloading hackathon-organizer-guide.md...
  Uploading hackathon-organizer-guide.md...
✅ hackathon-organizer-guide.md uploaded

  [... same for other files ...]

====================================
🎉 Setup complete!
====================================

Store name: fileSearchStores/abc123xyz

Add this to your .env file:
FILE_SEARCH_STORE_NAME=fileSearchStores/abc123xyz
```

**Say:**
```
Indexing happens asynchronously.
Gemini is now:
- Chunking these docs
- Creating embeddings
- Building the vector index

For large doc sets, you'd poll until complete.
For our 4 small files, it's ready immediately.

Copy that store name!
```

**Add to .env:**

```bash
FILE_SEARCH_STORE_NAME=fileSearchStores/abc123xyz
```

### Test Query from CLI (8 min)

**Say:**
```
Before building a UI, let's test queries from command line.
Good practice: verify the RAG works before adding UI complexity.
```

**Create query_test.py:**

```python
#!/usr/bin/env python3
"""
CLI tool to test RAG queries.

Usage:
    python query_test.py "Your question here"
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def query_rag(store_name: str, query: str):
    """Query the RAG system and return the response."""
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Create File Search tool
    file_search_tool = types.Tool(
        file_search=types.FileSearch(
            file_search_store_names=[store_name]
        )
    )
    
    # Generate response
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=query,
        config=types.GenerateContentConfig(
            tools=[file_search_tool],
        )
    )
    
    return response

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_test.py \"Your question\"")
        sys.exit(1)
    
    query = sys.argv[1]
    store_name = os.getenv("FILE_SEARCH_STORE_NAME")
    
    if not store_name:
        print("❌ FILE_SEARCH_STORE_NAME not in .env")
        sys.exit(1)
    
    print(f"🔍 Query: {query}")
    print(f"📚 Store: {store_name}")
    print("="*60 + "\n")
    
    response = query_rag(store_name, query)
    
    print("💬 Response:")
    print(response.text)
    
    # Print grounding metadata if available
    if response.candidates:
        candidate = response.candidates[0]
        grounding = getattr(candidate, "grounding_metadata", None)
        if grounding:
            chunks = getattr(grounding, "grounding_chunks", None)
            if chunks:
                print("\n" + "="*60)
                print(f"📎 Sources ({len(chunks)} chunks retrieved):\n")
                for i, chunk in enumerate(chunks, 1):
                    ctx = getattr(chunk, "retrieved_context", None)
                    if ctx:
                        title = getattr(ctx, "title", "Unknown")
                        uri = getattr(ctx, "uri", "")
                        print(f"  {i}. {title}")
                        if uri:
                            print(f"     URI: {uri}")
                    print()

if __name__ == "__main__":
    main()
```

**Test it:**

```bash
python query_test.py "How do I get reimbursed for a Hack Day?"
```

**Expected output:**

```
🔍 Query: How do I get reimbursed for a Hack Day?
📚 Store: fileSearchStores/abc123xyz456
============================================================

💬 Response:
To get reimbursed for a Hack Day, you need to submit receipts for approved expenses to MLH within 30 days of your event. Approved expenses typically include venue costs, food, and supplies. Make sure to check the Hack Day organizer guide for the complete list of reimbursable items.

============================================================
📎 Sources (2 chunks retrieved):

  1. hack-days-guide.md
     URI: ...

  2. hack-days-guide.md
     URI: ...
```

**Say:**
```
Look at that! 
- Accurate answer grounded in docs
- Citations show EXACTLY where it came from
- We can click through to verify

This is RAG working perfectly.

Try more questions: [ask chat for suggestions]
```

### Transition (2 min)

```
The RAG pipeline is working!

Now let's see what happens with different queries:
- Good questions vs bad questions
- How chunking affects retrieval
- Edge cases

Then we'll build the Streamlit UI.
```

**Common Pitfalls:**
- Indexing failures: check internet connection, API quotas
- Citation format varies (graceful fallback)
- Store name typos (copy-paste from output)

---

## 🔬 Segment 5: Explore & Experiment (1:00–1:15)

**Goal:** Try different queries, explain retrieval behavior, show RAG strengths/weaknesses

### Good Questions (5 min)

**Run these queries and explain why they work:**

```bash
# Specific policy question
python query_test.py "What are the requirements for an MLH member event?"
```

**Expected: Good answer with citations from policies.md**

**Say:**
```
Why this works:
- Specific entity (MLH member event)
- Likely in policies doc
- Clear, factual question

Perfect for RAG!
```

---

```bash
# Procedural "how-to"
python query_test.py "What steps do I follow to organize a hackathon?"
```

**Expected: Step-by-step answer from hackathon-guide.md**

**Say:**
```
Multi-step procedures are great for RAG.
The model can synthesize across multiple chunks.

Notice: Citations from different parts of the same doc.
```

---

```bash
# Code of conduct question
python query_test.py "What happens if someone violates the code of conduct?"
```

**Expected: Policy answer from code-of-conduct.md**

**Say:**
```
Sensitive policy question.
You NEED grounded answers here — no hallucination allowed.

RAG ensures you're quoting actual policy.
```

### Bad Questions (5 min)

**Try these and explain why they fail:**

```bash
# Out-of-scope question
python query_test.py "What is the weather in San Francisco?"
```

**Expected: "I don't have that information" or generic answer**

**Say:**
```
Not in the docs!

Good RAG systems should say "I don't know" instead of making things up.

You can tune this with system instructions.
```

---

```bash
# Vague question
python query_test.py "Tell me about MLH"
```

**Expected: Generic answer, maybe pulls random chunks**

**Say:**
```
Too broad. Retrieval might grab unrelated chunks.

Better question: "What is MLH's mission?" (specific)
```

---

```bash
# Opinion/speculation
python query_test.py "Is MLH better than other hackathon organizers?"
```

**Expected: Refuses or gives factual comparison**

**Say:**
```
Opinion questions don't have grounded answers.

RAG is for FACTS, not opinions.
```

### How Chunking Affects Retrieval (3 min)

**Explain with examples:**

```
Imagine this doc:

"MLH Fellowship is a 12-week program. Fellows work on open source.
The program includes mentorship and stipends."

Chunked as:
Chunk 1: "MLH Fellowship is a 12-week program. Fellows work on open source."
Chunk 2: "The program includes mentorship and stipends."

Query: "How long is the MLH Fellowship?"
→ Retrieves Chunk 1 ✅

Query: "Does MLH Fellowship pay?"
→ Might miss Chunk 2 if embedding isn't close enough ❌
→ Or retrieves both ✅ (depends on overlap/Top-K)

This is why chunk size and overlap matter!
Gemini File Search handles this automatically.
```

**Say:**
```
Manual RAG: You tune chunk size, overlap, Top-K
Gemini File Search: Optimized automatically

Trade-off: Less control, but way faster to build.
```

### Edge Cases (2 min)

**Try these:**

```bash
# Multi-part question
python query_test.py "What are the requirements for a Hack Day and how do I get reimbursed?"
```

**Expected: Answers both parts, or focuses on one**

**Say:**
```
The model can handle compound questions.
But single-topic queries often work better.

If this fails, break into two queries.
```

---

```bash
# Contradictory docs (if you have them)
# Skip if not applicable
```

### Transition (1 min)

```
You now understand:
- What RAG can and can't do
- How to craft good queries
- How retrieval works

Time to build the UI!
```

**Common Pitfalls:**
- Don't spend too long here (time check!)
- Cherry-pick queries that demonstrate principles
- If something breaks, explain why (teaching moment)

---

## 🎨 Segment 6: Streamlit Chat UI (1:15–1:40)

**Goal:** Build full chat interface with streaming, citations, and session state

### Streamlit Basics (5 min)

**Create app.py skeleton:**

```python
import streamlit as st

st.title("💬 MLH Doc Assistant")

# Chat input
user_input = st.chat_input("Ask a question...")

if user_input:
    st.write(f"You asked: {user_input}")
```

**Run it:**

```bash
streamlit run app.py
```

**Say:**
```
Streamlit auto-opens browser at localhost:8501.

Every time you save app.py, it reloads.
Fast iteration loop!
```

**Show the interface:**
- Chat input at bottom
- Messages display above
- Minimal code!

### Add Chat Messages (5 min)

**Update app.py:**

```python
import streamlit as st

st.title("💬 MLH Doc Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask a question...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # TODO: Add assistant response
    with st.chat_message("assistant"):
        st.write("I'll respond here!")
```

**Explain:**

```
st.session_state:
- Persists data between reruns
- Like React state
- Stores conversation history

st.chat_message():
- Renders message bubbles
- role: "user" or "assistant"
```

**Test:** Type a message, see it appear!

### Integrate RAG (10 min)

**Add RAG query function:**

```python
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found")
        st.stop()
    return genai.Client(api_key=api_key)

def query_rag_streaming(client, store_name, query):
    """Stream response and return sources."""
    file_search_tool = types.Tool(
        file_search=types.FileSearch(
            file_search_store_names=[store_name]
        )
    )
    
    stream = client.models.generate_content_stream(
        model='gemini-2.5-flash',
        contents=query,
        config=types.GenerateContentConfig(
            tools=[file_search_tool],
        )
    )
    
    for chunk in stream:
        if hasattr(chunk, 'text') and chunk.text:
            yield chunk.text
        
        # Extract grounding metadata (usually in final chunk)
        if hasattr(chunk, 'candidates') and chunk.candidates:
            candidate = chunk.candidates[0]
            grounding = getattr(candidate, "grounding_metadata", None)
            if grounding:
                chunks_list = getattr(grounding, "grounding_chunks", None)
                if chunks_list:
                    sources = []
                    for gc in chunks_list:
                        ctx = getattr(gc, "retrieved_context", None)
                        if ctx:
                            sources.append({
                                "title": getattr(ctx, "title", "Unknown"),
                                "uri": getattr(ctx, "uri", ""),
                            })
                    if sources:
                        yield {"sources": sources}
```

**Update the assistant response block:**

```python
if user_input:
    store_name = os.getenv("FILE_SEARCH_STORE_NAME")
    if not store_name:
        st.error("⚠️ Add FILE_SEARCH_STORE_NAME to .env")
        st.stop()
    
    # [user message code same as before...]
    
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        sources = []
        
        client = get_gemini_client()
        
        for chunk in query_rag_streaming(client, store_name, user_input):
            if isinstance(chunk, dict) and "sources" in chunk:
                sources = chunk["sources"]
            else:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
        # Store in history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "sources": sources,
        })
```

**Test:** Ask a question, see it stream!

**Say:**
```
Streaming is CRITICAL for good UX.
Users see progress, not a loading spinner.

The "▌" cursor makes it feel like typing.
```

### Add Citations Display (5 min)

**Update chat history display:**

```python
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources
        if "sources" in message and message["sources"]:
            with st.expander(f"📎 View {len(message['sources'])} source(s)"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**{i}. {source['title']}**")
                    if source.get("uri"):
                        st.caption(source["uri"])
                    st.divider()
```

**And after generating new response:**

```python
if sources:
    with st.expander(f"📎 View {len(sources)} source(s)"):
        for i, source in enumerate(sources, 1):
            st.markdown(f"**{i}. {source['title']}**")
            if source.get("uri"):
                st.caption(source["uri"])
            st.divider()
```

**Test:** Citations appear in expandable section!

### Sidebar Features (5 min)

**Add sidebar:**

```python
with st.sidebar:
    st.title("🎓 MLH Doc Assistant")
    st.markdown("Ask questions about MLH documentation")
    
    st.divider()
    
    # Example questions
    st.subheader("💡 Try asking:")
    examples = [
        "How do I get reimbursed for a Hack Day?",
        "What is MLH's code of conduct?",
        "How do I organize a hackathon?",
    ]
    
    for ex in examples:
        if st.button(ex, key=f"ex_{hash(ex)}", use_container_width=True):
            st.session_state.pending_question = ex
    
    st.divider()
    
    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
```

**Handle pending question:**

```python
# At the top of main section:
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if st.session_state.pending_question:
    user_input = st.session_state.pending_question
    st.session_state.pending_question = None
else:
    user_input = st.chat_input("Ask a question...")
```

**Test:** Click example question, see it auto-ask!

### Transition (1 min)

```
We have a working chat UI!
Let's add polish: error handling, loading states, better UX.
```

**Common Pitfalls:**
- Session state bugs: always initialize before use
- Streaming issues: test with different queries
- Rerun timing: Streamlit reruns on every interaction

---

## ✨ Segment 7: Polish & Extend (1:40–1:50)

**Goal:** Add error handling, loading spinner, better UX

### Error Handling (3 min)

**Wrap RAG call in try/except:**

```python
try:
    client = get_gemini_client()
    
    for chunk in query_rag_streaming(client, store_name, user_input):
        # [same as before...]
        
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()
```

**Test:** Break API key in .env, see error message

**Say:**
```
Production apps need graceful failures.
Don't crash — show helpful messages.
```

### Loading Spinner (2 min)

**Add spinner during retrieval:**

```python
with st.chat_message("assistant"):
    with st.spinner("🔍 Searching docs..."):
        message_placeholder = st.empty()
        # [rest of code...]
```

**Test:** See spinner while waiting!

### Welcome Message (2 min)

**Add at the end:**

```python
if not st.session_state.messages:
    st.info("👋 Welcome! Ask me about MLH's documentation.")
```

### Store Name Input in Sidebar (2 min)

**Add to sidebar:**

```python
with st.sidebar:
    # [existing code...]
    
    st.divider()
    
    store_name_input = st.text_input(
        "FileSearchStore Name",
        value=os.getenv("FILE_SEARCH_STORE_NAME", ""),
        help="From setup_store.py output"
    )
    
    if not store_name_input:
        st.warning("⚠️ Enter store name above")
```

**Update query to use:**

```python
store_name = store_name_input or os.getenv("FILE_SEARCH_STORE_NAME")
```

### Show How to Swap Docs (2 min)

**Open setup_store.py and edit MLH_DOCS:**

```python
# Replace with your own docs:
MY_DOCS = {
    "my-doc.md": "https://raw.githubusercontent.com/yourorg/repo/main/doc.md",
}
```

**Say:**
```
That's it! Run setup_store.py again with new URLs.
Same app works with ANY documentation.

Ideas:
- Company internal wiki
- Project READMEs
- Course materials
- Research papers

Build once, reuse everywhere.
```

### Transition (1 min)

```
The app is done!

Let's do a live demo with audience questions.
```

**Common Pitfalls:**
- Don't add too many features (time constraint)
- Focus on polish that matters: errors, loading, clarity

---

## 🎉 Segment 8: Wrap Up (1:50–2:00)

**Goal:** Live demo, Q&A, recap, next steps

### Live Demo with Audience (5 min)

**Ask chat for questions:**

```
"Drop questions in chat and I'll ask the bot!"

[Take 3-5 questions from audience]

Examples:
- "What are hack days?"
- "How does MLH support organizers?"
- "Can we use MLH branding?"
```

**Show:**
- Real-time answers
- Citations
- Different doc sources

### Recap (3 min)

**What we built:**

```
✅ FileSearchStore with MLH docs
✅ RAG query function with citations
✅ Streamlit chat interface
✅ Streaming responses
✅ Error handling and UX polish

~200 lines of Python
Zero ML code
Production-ready RAG
```

**What you learned:**

```
✅ What RAG is and why it matters
✅ How chunking, embeddings, and retrieval work
✅ Gemini File Search API
✅ Streamlit basics (chat components, session state)
✅ Streaming for better UX
```

### Next Steps (2 min)

**For this app:**

```
1. Deploy it:
   - Streamlit Cloud (free): streamlit.io/cloud
   - Railway, Render, Fly.io
   
2. Extend it:
   - Add conversation memory (use chat history)
   - Multi-turn clarifying questions
   - Feedback buttons (👍👎)
   - Analytics (which docs get queried most?)
   
3. Use your own docs:
   - Edit setup_store.py
   - Run it
   - Same app, different knowledge base!
```

**For your MLH project:**

```
Hackathon ideas using this tech:
- Internal company knowledge base bot
- Course assistant for students
- Customer support automation
- Research paper Q&A
- Legal document search

Same pattern, different domain!
```

### Resources (1 min)

**Show on screen:**

```
🔗 Links:

Repo: github.com/wei/mlh-gemini-rag-workshop
Tutorial: [link to WORKSHOP.md]
Gemini Docs: ai.google.dev/gemini-api/docs/file-search
MLH: ghw.mlh.io

🙋 Questions? Ask in:
- MLH Discord
- GitHub Issues
- Twitter: @yourhandle
```

### Final Words (1 min)

```
Thanks for joining!

Remember:
- RAG solves hallucination
- Gemini File Search makes it EASY
- You can build production apps in an afternoon

Go build something cool! 🚀

See you at the next MLH event!
```

**Common Pitfalls:**
- Watch the clock! Leave time for Q&A
- Have backup questions if chat is quiet
- End on time (respect audience schedules)

---

## Post-Stream Checklist

- [ ] Upload recording to YouTube
- [ ] Share code on GitHub
- [ ] Post highlights on Twitter/LinkedIn
- [ ] Answer questions in Discord
- [ ] Update repo README with recording link
- [ ] Share in MLH Slack/Discord

---

## Emergency Backup Plan

**If catastrophic failure:**

1. **API quota hit:**
   - Switch to backup API key
   - Or use finished code (pre-tested)

2. **Internet dies:**
   - Have finished app running locally
   - Screen record in advance as backup

3. **Code breaks live:**
   - Don't panic! Explain error
   - Switch to finished version
   - Debugging is educational

4. **Time runs over:**
   - Skip "Explore & Experiment" section
   - Go straight from CLI test → Streamlit UI
   - Save polish for post-stream tutorial

**Remember:** Mistakes are teaching moments. Audience appreciates authenticity.

---

## Engagement Tips

### Throughout Stream:
- Ask questions: "Anyone built with RAG before?"
- Read chat: "Great question, Sarah!"
- Show errors: "Oops, forgot to save. Always save!"
- Use analogies: "Vector search is like Google for meaning"
- Celebrate wins: "Look at that! Perfect answer!"

### Keep Energy High:
- Stand while streaming (if possible)
- Vary voice tone
- Show genuine excitement about RAG
- Take 5-second pauses to breathe
- Smile (even if just voice)

### Technical Tips:
- Zoom in on terminal (huge font)
- Use syntax highlighting in editor
- Have water nearby
- Bathroom break before stream
- Test mic/camera before going live

---

**Good luck! You've got this! 🎓🚀**
