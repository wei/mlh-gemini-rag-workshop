# Build a RAG-Powered Documentation Assistant

**Duration:** ~2 hours  
**Difficulty:** Beginner-friendly  
**Stack:** Python + Streamlit + Gemini File Search

Welcome! By the end of this workshop, you'll have built a chatbot that answers questions about MLH's documentation with **zero hallucinations** — every answer will be grounded in actual docs with citations.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [What is RAG?](#what-is-rag)
3. [Setup Your Environment](#setup-your-environment)
4. [Test the Gemini API](#test-the-gemini-api)
5. [Build the RAG Pipeline](#build-the-rag-pipeline)
6. [Test from Command Line](#test-from-command-line)
7. [Build the Streamlit UI](#build-the-streamlit-ui)
8. [Add Polish & Features](#add-polish--features)
9. [Try It Yourself Challenges](#try-it-yourself-challenges)
10. [Troubleshooting](#troubleshooting)
11. [Next Steps](#next-steps)

---

## Prerequisites

### Required

- **Python 3.10 or higher**
  ```bash
  python --version  # Should show 3.10+
  ```

- **pip** (Python package manager, comes with Python)

- **Google AI Studio API Key** (free)
  - Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
  - Sign in with your Google account
  - Click "Create API Key"
  - Copy and save it somewhere safe

- **Text editor or IDE** (VS Code, PyCharm, Sublime, etc.)

- **Terminal/Command Prompt**

### Optional

- Git (for cloning the repo)
- Basic knowledge of Python (functions, imports, loops)
- Familiarity with command line basics

### No Prior Knowledge Needed

- Machine learning or AI
- Vector databases
- Streamlit
- RAG concepts (we'll teach you!)

---

## What is RAG?

Before we code, let's understand **why** we need RAG.

### The Problem: LLM Hallucination

Try asking ChatGPT or Gemini:

> "What are the requirements for an MLH Hack Day?"

You'll get a plausible-sounding answer, but:
- ❌ It might be outdated (training data has a cutoff date)
- ❌ It might be wrong (models "make up" info they don't know)
- ❌ You can't verify the source

This is called **hallucination** — the model generates confident but incorrect information.

### The Solution: RAG

**Retrieval-Augmented Generation (RAG)** solves this by:

1. **Storing** your documents in a searchable format
2. **Retrieving** relevant sections when a user asks a question
3. **Generating** an answer using ONLY those retrieved sections

**Result:** Grounded, verifiable answers with citations.

### How RAG Works (5 Steps)

#### Step 1: Chunking

Break documents into smaller pieces:

```
Original Doc (5000 words):
"MLH Fellowship is a 12-week program for students..."

↓

Chunks (500-1000 words each):
- Chunk 1: "MLH Fellowship is a 12-week program..."
- Chunk 2: "...program includes mentorship and stipends..."
- Chunk 3: "...application process opens in November..."
```

**Why?** LLMs have context limits (can't fit entire docs).

#### Step 2: Embeddings

Convert text to numerical vectors:

```
Text: "MLH Hack Day reimbursement"
  ↓
Embedding: [0.23, -0.45, 0.67, ..., 0.12]  (768 numbers)
```

**Why?** Computers can't compare "meaning" of text directly, but they can compare vectors.

**Magic:** Similar meanings → similar vectors (close together in space)

```
"cat" is close to "kitten" in vector space
"cat" is far from "car" in vector space
```

#### Step 3: Vector Database

Store all chunk embeddings in a special database:

```
Database:
- Chunk 1 → [0.18, -0.52, ...]
- Chunk 2 → [0.91, 0.23, ...]
- Chunk 3 → [-0.44, 0.77, ...]
...
```

**Why?** Fast similarity search (find closest vectors).

#### Step 4: Retrieval

When user asks a question:

```
User: "How do I get reimbursed?"
  ↓
1. Embed the question: [0.19, -0.51, 0.70, ...]
2. Search database for closest chunk vectors
3. Return Top-K (e.g., 5) most similar chunks
```

**Example result:**
```
Chunks retrieved:
1. "...reimbursement requires receipts..." (similarity: 0.92)
2. "...submit to hackdays@mlh.io..." (similarity: 0.87)
3. "...approved expenses include venue..." (similarity: 0.81)
```

#### Step 5: Generation

Send retrieved chunks + question to LLM:

```
Prompt to LLM:
"Use only these documents to answer:

[Chunk 1]: ...reimbursement requires receipts...
[Chunk 2]: ...submit to hackdays@mlh.io...
[Chunk 3]: ...approved expenses include venue...

Question: How do I get reimbursed?

Answer:"
```

LLM generates grounded answer + cites sources.

### What Gemini File Search Does

Normally you'd need to:
- Choose chunking strategy (size, overlap)
- Generate embeddings (OpenAI, Cohere, etc.)
- Set up vector DB (Pinecone, Weaviate, Chroma)
- Write retrieval logic
- Parse citations

**Gemini File Search automates ALL of this:**

```python
# That's it!
client.vector_stores.create()
client.files.upload(...)
response = client.generate_content(query, tools=[file_search_tool])
```

No separate services, no chunking code, no embedding management. 🎉

---

## Setup Your Environment

### 1. Create Project Directory

```bash
mkdir mlh-rag-workshop
cd mlh-rag-workshop
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

**Why virtual environments?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Easy to delete and recreate

### 3. Install Dependencies

Create `requirements.txt`:

```txt
google-genai>=1.0.0
streamlit>=1.30.0
python-dotenv>=1.0.0
requests>=2.31.0
```

Install:

```bash
pip install -r requirements.txt
```

**What these packages do:**
- `google-genai`: Official Gemini API SDK
- `streamlit`: Web UI framework (chat interface in 10 lines!)
- `python-dotenv`: Load API keys from `.env` file
- `requests`: Download docs from GitHub

### 4. Configure API Key

Create `.env` file:

```bash
touch .env
```

Add your API key:

```bash
GEMINI_API_KEY=your-api-key-here
```

**Important:** Don't share this file! Add to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

---

## Test the Gemini API

Before building RAG, let's verify the API works.

### Create `test.py`

```python
#!/usr/bin/env python3
"""
Test that Gemini API is working.
"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file")
    print("   Get your key from https://aistudio.google.com/apikey")
    exit(1)

print("✅ API key loaded")

# Create Gemini client
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

### Run It

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

**What just happened?**

1. `load_dotenv()` read your `.env` file
2. `genai.Client(api_key=...)` authenticated with Gemini
3. `generate_content(...)` sent a prompt and got a response
4. `response.text` extracted the generated text

**If it failed:** Check [Troubleshooting](#troubleshooting)

---

## Build the RAG Pipeline

Now the fun part: creating a vector store and uploading documents.

### Create `setup_store.py`

This script will:
1. Create a FileSearchStore (vector database)
2. Download MLH docs from GitHub
3. Upload and index them
4. Print a store name you'll use in your app

```python
#!/usr/bin/env python3
"""
Setup script to create FileSearchStore and upload MLH documentation.

Run this once:
    python setup_store.py
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

# MLH documentation URLs (raw markdown from GitHub)
MLH_DOCS = {
    "hackathon-organizer-guide.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/main/README.md",
    "mlh-policies.md": "https://raw.githubusercontent.com/MLH/mlh-policies/main/README.md",
    "code-of-conduct.md": "https://raw.githubusercontent.com/MLH/mlh-policies/main/code-of-conduct.md",
    "hack-days-guide.md": "https://raw.githubusercontent.com/MLH/mlh-hack-days-organizer-guide/main/README.md",
}


def download_file(url: str, filename: str, temp_dir: Path) -> Path:
    """Download a file from URL to temp directory."""
    print(f"  📥 Downloading {filename}...")
    response = requests.get(url)
    response.raise_for_status()
    
    file_path = temp_dir / filename
    file_path.write_text(response.text, encoding='utf-8')
    return file_path


def wait_for_indexing(client: genai.Client, store_name: str, timeout: int = 300):
    """Poll the store until indexing is complete."""
    print("\n⏳ Waiting for indexing to complete...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        store = client.vector_stores.get(name=store_name)
        
        # Check if all files are processed
        if hasattr(store, 'file_counts'):
            total = store.file_counts.total
            processed = store.file_counts.completed + store.file_counts.failed
            
            print(f"  Progress: {processed}/{total} files processed")
            
            if processed == total:
                if store.file_counts.failed > 0:
                    print(f"  ⚠️  {store.file_counts.failed} files failed to index")
                print("✅ Indexing complete!")
                return True
        
        time.sleep(5)
    
    print("⚠️  Timeout waiting for indexing")
    return False


def main():
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        print("   Get your key from https://aistudio.google.com/apikey")
        return
    
    client = genai.Client(api_key=api_key)
    
    # Step 1: Create FileSearchStore
    print("📦 Creating FileSearchStore...")
    store = client.vector_stores.create(
        config=types.CreateVectorStoreConfig(
            display_name="MLH Documentation Store",
        )
    )
    print(f"✅ Created store: {store.name}")
    
    # Step 2: Download and upload documents
    print("\n📥 Downloading and uploading MLH docs...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for filename, url in MLH_DOCS.items():
            try:
                # Download file
                file_path = download_file(url, filename, temp_path)
                
                # Upload to Gemini Files API
                print(f"  ☁️  Uploading {filename} to Gemini...")
                uploaded_file = client.files.upload(file=str(file_path))
                
                # Add file to vector store
                print(f"  🗂️  Adding {filename} to store...")
                client.vector_stores.add_files(
                    vector_store=store.name,
                    files=[uploaded_file.name]
                )
                
                print(f"✅ {filename} indexed\n")
                
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}\n")
    
    # Step 3: Wait for indexing
    wait_for_indexing(client, store.name)
    
    # Step 4: Print final instructions
    print("\n" + "="*60)
    print("🎉 Setup complete!")
    print("="*60)
    print(f"\nStore Name: {store.name}")
    print("\n📝 Next steps:")
    print("1. Copy the store name above")
    print("2. Add it to your .env file:")
    print(f"   FILE_SEARCH_STORE_NAME={store.name}")
    print("3. Test it:")
    print(f'   python query_test.py "How do I get reimbursed for a Hack Day?"')
    print()


if __name__ == "__main__":
    main()
```

### Run It

```bash
python setup_store.py
```

**Expected output:**

```
📦 Creating FileSearchStore...
✅ Created store: vectorstores/abc123xyz456

📥 Downloading and uploading MLH docs...
  📥 Downloading hackathon-organizer-guide.md...
  ☁️  Uploading hackathon-organizer-guide.md to Gemini...
  🗂️  Adding hackathon-organizer-guide.md to store...
✅ hackathon-organizer-guide.md indexed

  [... same for other files ...]

⏳ Waiting for indexing to complete...
  Progress: 4/4 files processed
✅ Indexing complete!

============================================================
🎉 Setup complete!
============================================================

Store Name: vectorstores/abc123xyz456

📝 Next steps:
1. Copy the store name above
2. Add it to your .env file:
   FILE_SEARCH_STORE_NAME=vectorstores/abc123xyz456
3. Test it:
   python query_test.py "How do I get reimbursed for a Hack Day?"
```

**What happened behind the scenes?**

1. Created a new vector store (empty database)
2. Downloaded MLH markdown files from GitHub
3. Uploaded each file to Gemini Files API
4. Added files to the vector store
5. Gemini automatically:
   - Chunked the documents
   - Generated embeddings
   - Indexed them for fast search

**Copy the store name** and add to `.env`:

```bash
FILE_SEARCH_STORE_NAME=vectorstores/abc123xyz456
```

Replace `abc123xyz456` with your actual store name!

---

## Test from Command Line

Before building a UI, let's test that RAG works.

### Create `query_test.py`

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

# Load environment variables
load_dotenv()


def query_rag(store_name: str, query: str) -> tuple[str, list]:
    """
    Query the RAG system and return response text + citations.
    
    Args:
        store_name: The FileSearchStore name (e.g., "vectorstores/abc123")
        query: The user's question
    
    Returns:
        Tuple of (response_text, citations_list)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    
    client = genai.Client(api_key=api_key)
    
    # Create File Search tool with the store
    file_search_tool = types.Tool(
        file_search=types.FileSearch(
            vector_store_names=[store_name]
        )
    )
    
    # Generate response with RAG
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=query,
        config=types.GenerateContentConfig(
            tools=[file_search_tool],
            response_modalities=["TEXT"],
        )
    )
    
    # Extract text
    text = response.text
    
    # Extract citations from grounding metadata
    citations = []
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'grounding_metadata'):
            metadata = candidate.grounding_metadata
            if hasattr(metadata, 'file_citations'):
                for citation in metadata.file_citations:
                    citations.append({
                        'source': citation.file_name if hasattr(citation, 'file_name') else 'Unknown',
                        'text': citation.text if hasattr(citation, 'text') else ''
                    })
    
    return text, citations


def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("❌ Error: Missing query argument")
        print("\nUsage:")
        print('  python query_test.py "Your question here"')
        print("\nExample:")
        print('  python query_test.py "How do I organize a hackathon?"')
        sys.exit(1)
    
    query = sys.argv[1]
    
    # Get store name from environment
    store_name = os.getenv("FILE_SEARCH_STORE_NAME")
    if not store_name:
        print("❌ Error: FILE_SEARCH_STORE_NAME not found in .env file")
        print("   Run setup_store.py first and add the store name to .env")
        sys.exit(1)
    
    # Execute query
    print(f"🔍 Query: {query}")
    print(f"📚 Store: {store_name}")
    print("\n" + "="*60 + "\n")
    
    try:
        text, citations = query_rag(store_name, query)
        
        # Print response
        print("💬 Response:")
        print(text)
        
        # Print citations
        if citations:
            print("\n" + "="*60)
            print(f"📎 Citations ({len(citations)}):\n")
            for i, citation in enumerate(citations, 1):
                print(f"{i}. {citation['source']}")
                if citation['text']:
                    # Show first 150 chars of cited text
                    preview = citation['text'][:150]
                    if len(citation['text']) > 150:
                        preview += "..."
                    print(f'   "{preview}"')
                print()
        else:
            print("\n(No citations found)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Test It

```bash
python query_test.py "How do I get reimbursed for a Hack Day?"
```

**Expected output:**

```
🔍 Query: How do I get reimbursed for a Hack Day?
📚 Store: vectorstores/abc123xyz456

============================================================

💬 Response:
To get reimbursed for a Hack Day, you need to submit receipts for approved expenses to MLH within 30 days of your event. Approved expenses typically include venue costs, food, and supplies. Make sure to check the Hack Day organizer guide for the complete list of reimbursable items and the submission process.

============================================================
📎 Citations (2):

1. hack-days-guide.md
   "Reimbursement requires submission of itemized receipts within 30 days. Approved expenses include venue rental, catering, and event supplies up to $500..."

2. hack-days-guide.md
   "To ensure timely reimbursement, email receipts to hackdays@mlh.io with your event name and date in the subject line..."
```

**🎉 It works!** Notice:
- Answer is grounded in actual docs
- Citations show exactly where info came from
- You can verify the response is accurate

### Try More Queries

```bash
python query_test.py "What is MLH's code of conduct?"
python query_test.py "What are the requirements for an MLH member event?"
python query_test.py "How do I organize a hackathon?"
```

**What's happening under the hood?**

1. Your query is embedded into a vector
2. Gemini searches the vector store for similar chunks
3. Top-K most relevant chunks are retrieved
4. Chunks + query are sent to the LLM
5. LLM generates answer grounded in those chunks
6. Citations are extracted from metadata

**All automatic!** ✨

---

## Build the Streamlit UI

CLI works, but a chat interface is way better UX. Let's build one!

### Basic Streamlit App

Create `app.py`:

```python
import streamlit as st

st.title("💬 MLH Documentation Assistant")

# Chat input
user_input = st.chat_input("Ask a question about MLH...")

if user_input:
    st.write(f"You asked: {user_input}")
```

Run it:

```bash
streamlit run app.py
```

Your browser should open to `http://localhost:8501`.

**You'll see:**
- Title at the top
- Chat input at the bottom
- Type something → see "You asked: ..."

**Streamlit auto-reloads** when you save `app.py`. Fast iteration!

### Add Chat Messages

Update `app.py`:

```python
import streamlit as st

st.title("💬 MLH Documentation Assistant")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask a question about MLH...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Placeholder for assistant response
    with st.chat_message("assistant"):
        st.write("I'll respond here soon!")
    
    # Add placeholder to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": "I'll respond here soon!"
    })
```

**What changed?**

- `st.session_state.messages`: Persists conversation between reruns
- `st.chat_message()`: Renders message bubbles (user vs assistant)
- Messages are stored and redisplayed on each rerun

**Test it:** Type messages, see conversation build up!

### Integrate RAG

Now let's make it actually answer questions with RAG.

**Full `app.py`:**

```python
#!/usr/bin/env python3
"""
MLH Documentation Assistant - RAG-powered chatbot with Streamlit.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="MLH Doc Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []


def get_gemini_client():
    """Initialize and return Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in .env file")
        st.stop()
    return genai.Client(api_key=api_key)


def query_rag_streaming(client: genai.Client, store_name: str, query: str):
    """
    Query the RAG system with streaming.
    
    Yields chunks of text as they arrive.
    Returns citations in the final chunk.
    """
    if not store_name:
        raise ValueError("Store name is required")
    
    # Create File Search tool
    file_search_tool = types.Tool(
        file_search=types.FileSearch(
            vector_store_names=[store_name]
        )
    )
    
    # Stream the response
    stream = client.models.generate_content_stream(
        model='gemini-2.5-flash',
        contents=query,
        config=types.GenerateContentConfig(
            tools=[file_search_tool],
            response_modalities=["TEXT"],
        )
    )
    
    # Yield text chunks
    citations = []
    
    for chunk in stream:
        if hasattr(chunk, 'text') and chunk.text:
            yield chunk.text
        
        # Extract citations from the final chunk
        if hasattr(chunk, 'candidates') and chunk.candidates:
            candidate = chunk.candidates[0]
            if hasattr(candidate, 'grounding_metadata'):
                metadata = candidate.grounding_metadata
                if hasattr(metadata, 'file_citations'):
                    for citation in metadata.file_citations:
                        citations.append({
                            'source': citation.file_name if hasattr(citation, 'file_name') else 'Unknown',
                            'text': citation.text if hasattr(citation, 'text') else ''
                        })
    
    # Return citations as a special marker
    if citations:
        yield {"citations": citations}


# Main chat interface
st.title("💬 Chat with MLH Documentation")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display citations if present
        if "citations" in message and message["citations"]:
            with st.expander(f"📎 View {len(message['citations'])} citation(s)"):
                for i, citation in enumerate(message["citations"], 1):
                    st.markdown(f"**{i}. {citation['source']}**")
                    if citation.get('text'):
                        preview = citation['text'][:200] + "..." if len(citation['text']) > 200 else citation['text']
                        st.caption(f'"{preview}"')
                    st.divider()

# Chat input
user_input = st.chat_input("Ask a question about MLH...")

if user_input:
    # Get store name
    store_name = os.getenv("FILE_SEARCH_STORE_NAME")
    if not store_name:
        st.error("⚠️ FILE_SEARCH_STORE_NAME not found in .env file")
        st.stop()
    
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        citations = []
        
        try:
            client = get_gemini_client()
            
            # Stream the response
            for chunk in query_rag_streaming(client, store_name, user_input):
                if isinstance(chunk, dict) and "citations" in chunk:
                    # Store citations
                    citations = chunk["citations"]
                else:
                    # Append text chunk
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
            
            # Final update without cursor
            message_placeholder.markdown(full_response)
            
            # Display citations
            if citations:
                with st.expander(f"📎 View {len(citations)} citation(s)"):
                    for i, citation in enumerate(citations, 1):
                        st.markdown(f"**{i}. {citation['source']}**")
                        if citation.get('text'):
                            preview = citation['text'][:200] + "..." if len(citation['text']) > 200 else citation['text']
                            st.caption(f'"{preview}"')
                        st.divider()
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "citations": citations
            })
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()

# Show welcome message if no messages yet
if not st.session_state.messages:
    st.info("👋 Welcome! Ask me anything about MLH's documentation.")
```

### Test It

1. Save `app.py`
2. Streamlit will auto-reload
3. Ask: "How do I get reimbursed for a Hack Day?"
4. Watch the response stream in!
5. Click "View citations" to see sources

**🎉 You have a working RAG chatbot!**

---

## Add Polish & Features

Let's make it even better.

### Add Sidebar with Examples

Add before `st.title(...)`:

```python
# Sidebar
with st.sidebar:
    st.title("🎓 MLH Doc Assistant")
    st.markdown("Ask questions about MLH documentation!")
    
    st.divider()
    
    # Example questions
    st.subheader("💡 Try asking:")
    example_questions = [
        "How do I get reimbursed for a Hack Day?",
        "What are the requirements for an MLH member event?",
        "What is MLH's code of conduct?",
        "How do I organize a hackathon?",
        "What support does MLH provide to organizers?"
    ]
    
    for question in example_questions:
        if st.button(question, key=f"example_{hash(question)}", use_container_width=True):
            st.session_state.pending_question = question
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Built with Gemini File Search")
```

And add this near the top of the file (after session state init):

```python
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
```

And replace the `user_input = st.chat_input(...)` line with:

```python
# Handle pending question from sidebar
if st.session_state.pending_question:
    user_input = st.session_state.pending_question
    st.session_state.pending_question = None
else:
    user_input = st.chat_input("Ask a question about MLH...")
```

**Test it:** Click example questions in the sidebar!

### Add Loading Spinner

Wrap the streaming loop:

```python
with st.chat_message("assistant"):
    with st.spinner("🔍 Searching docs..."):
        message_placeholder = st.empty()
        # [rest of streaming code...]
```

### Add Error Handling

Already done! The `try/except` block catches errors and shows them gracefully.

---

## Try It Yourself Challenges

### Challenge 1: Add Conversation History

Right now, each query is independent. Make the bot remember previous messages.

**Hint:** Include `st.session_state.messages` in the prompt:

```python
# Build conversation history
conversation = []
for msg in st.session_state.messages[-6:]:  # Last 3 exchanges
    conversation.append(msg)
conversation.append({"role": "user", "content": user_input})

# Send to Gemini (adjust query_rag_streaming to accept history)
```

### Challenge 2: Add Feedback Buttons

Let users rate responses with 👍/👎:

```python
col1, col2 = st.columns(2)
with col1:
    if st.button("👍", key=f"up_{i}"):
        st.success("Thanks for the feedback!")
with col2:
    if st.button("👎", key=f"down_{i}"):
        st.warning("We'll improve!")
```

### Challenge 3: Use Your Own Docs

Edit `setup_store.py` to upload your own documentation:

```python
MY_DOCS = {
    "my-project-readme.md": "https://raw.githubusercontent.com/you/project/main/README.md",
    "my-api-docs.md": "https://raw.githubusercontent.com/you/project/main/docs/api.md",
}
```

Run `python setup_store.py` again, get a new store name, update `.env`.

### Challenge 4: Add System Instructions

Make the bot more concise or friendlier:

```python
config=types.GenerateContentConfig(
    system_instruction="You are a helpful MLH expert. Be concise and friendly. If you don't know, say so.",
    tools=[file_search_tool],
    response_modalities=["TEXT"],
)
```

### Challenge 5: Deploy It

Deploy to Streamlit Cloud (free!):

1. Push your code to GitHub (without `.env`)
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your repo
4. Add secrets (API key) in the dashboard
5. Deploy!

---

## Troubleshooting

### "GEMINI_API_KEY not found"

**Fix:**
1. Make sure `.env` file exists in project root
2. Check for typos: `GEMINI_API_KEY=...` (no spaces around `=`)
3. Make sure you're running scripts from project root

### "FILE_SEARCH_STORE_NAME not found"

**Fix:**
1. Run `python setup_store.py` first
2. Copy the output store name
3. Add to `.env`: `FILE_SEARCH_STORE_NAME=vectorstores/abc123xyz`

### "Rate limit exceeded"

**Fix:**
- Wait a few seconds between requests
- Gemini File Search has generous free tier limits
- For production, implement rate limiting

### No citations in response

**This is normal if:**
- Query doesn't require specific doc references
- Model generated a general answer
- Try more specific questions about policies/procedures

### Slow first query

**Normal!**
- First query initializes the client and loads the vector store
- Subsequent queries are much faster
- Consider adding a loading message

### Streamlit won't start

**Fix:**
```bash
# Make sure venv is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall Streamlit
pip install --upgrade streamlit

# Check port isn't in use
streamlit run app.py --server.port 8502
```

### ImportError: No module named 'google'

**Fix:**
```bash
# Make sure venv is activated
# Reinstall google-genai
pip install --upgrade google-genai
```

---

## Next Steps

### Learn More

**RAG Concepts:**
- [What is RAG? (Google Cloud)](https://cloud.google.com/use-cases/retrieval-augmented-generation)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)
- [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

**Gemini API:**
- [File Search Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- [Python SDK Docs](https://googleapis.github.io/python-genai/)
- [API Reference](https://ai.google.dev/api/rest)

**Streamlit:**
- [Streamlit Docs](https://docs.streamlit.io/)
- [Chat Elements Guide](https://docs.streamlit.io/develop/api-reference/chat)
- [Deployment Options](https://docs.streamlit.io/deploy)

### Build Something Cool

**Hackathon Project Ideas:**

1. **Company Knowledge Base Bot**
   - Upload internal docs, wikis, runbooks
   - Employees ask questions → get instant answers
   - Reduces support tickets

2. **Course Assistant**
   - Upload lecture notes, textbooks
   - Students ask questions → get explanations
   - Include citations to specific chapters

3. **Customer Support Bot**
   - Upload product manuals, FAQs
   - Customers ask questions → get help
   - Reduces support queue

4. **Research Paper Q&A**
   - Upload academic papers
   - Researchers ask questions → find relevant sections
   - Speeds up literature review

5. **Legal Document Search**
   - Upload contracts, policies, regulations
   - Lawyers ask questions → find clauses
   - Cite exact paragraphs

**The code is the same — just swap the docs!**

### Share Your Work

Built something cool? Share it!

- Post on Twitter/LinkedIn with #MLH #GeminiRAG
- Open source it on GitHub
- Submit to MLH showcase
- Present at next hack night

---

## Congratulations! 🎉

You've built a production-ready RAG system in ~2 hours.

**You learned:**
- ✅ What RAG is and why it matters
- ✅ How chunking, embeddings, and vector search work
- ✅ Gemini File Search API
- ✅ Streamlit chat interfaces
- ✅ Streaming for better UX
- ✅ Citation display

**You built:**
- ✅ Document indexing pipeline
- ✅ RAG query engine
- ✅ Chat UI with streaming
- ✅ Citation display
- ✅ ~200 lines of Python

Now go build something amazing! 🚀

---

**Made with ❤️ for MLH Global Hack Week**
