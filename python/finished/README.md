# Finished Implementation

This folder contains the complete, working RAG-powered doc assistant. Use this as a reference or to quickly get started.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Copy it

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
GEMINI_API_KEY=your-actual-api-key-here
```

### 4. Create the FileSearchStore

This downloads MLH docs and uploads them to Gemini:

```bash
python setup_store.py
```

This will:
- Create a new FileSearchStore
- Download MLH documentation from GitHub
- Upload and index the files
- Print a store name like `vectorstores/abc123xyz`

**Copy the store name** and add it to your `.env`:

```bash
FILE_SEARCH_STORE_NAME=vectorstores/abc123xyz
```

### 5. Test the RAG System (Optional)

Before building the UI, test queries from the command line:

```bash
python query_test.py "How do I get reimbursed for a Hack Day?"
```

You should see a response with citations!

### 6. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## File Overview

| File | Purpose |
|------|---------|
| `setup_store.py` | One-time setup: creates FileSearchStore and uploads docs |
| `query_test.py` | CLI tool to test RAG queries before building UI |
| `app.py` | Full Streamlit chat interface with streaming + citations |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for environment variables |

## How It Works

### RAG Pipeline

1. **Indexing** (`setup_store.py`)
   - Downloads MLH docs from GitHub
   - Uploads to Gemini Files API
   - Creates a FileSearchStore (vector database)
   - Gemini automatically chunks, embeds, and indexes

2. **Retrieval** (when you ask a question)
   - Your query is embedded
   - Gemini searches the FileSearchStore for relevant chunks
   - Top-k most similar chunks are retrieved

3. **Generation** 
   - Retrieved chunks + your query → sent to Gemini
   - Model generates a grounded response
   - Returns answer with citations

### Key Components

**File Search Tool:**
```python
file_search_tool = types.Tool(
    file_search=types.FileSearch(
        vector_store_names=[store_name]
    )
)
```

**Streaming Response:**
```python
stream = client.models.generate_content_stream(
    model='gemini-2.5-flash',
    contents=query,
    config=types.GenerateContentConfig(
        tools=[file_search_tool],
        response_modalities=["TEXT"],
    )
)
```

**Citations:**
```python
if hasattr(candidate, 'grounding_metadata'):
    metadata = candidate.grounding_metadata
    if hasattr(metadata, 'file_citations'):
        for citation in metadata.file_citations:
            # Process citation...
```

## Troubleshooting

### "GEMINI_API_KEY not found"

Make sure:
- You created a `.env` file (not `.env.example`)
- You added your actual API key
- No spaces around the `=` sign

### "Store name is required"

Either:
- Add `FILE_SEARCH_STORE_NAME` to your `.env` file, OR
- Enter the store name in the Streamlit sidebar

### "No citations found"

This is normal if:
- The model generated a generic response
- The answer didn't require specific document references
- Try a more specific question about MLH policies

### Slow first query

The first query after starting the app may be slow while:
- The client initializes
- The vector store loads
- Subsequent queries will be faster

## Customization Ideas

### Use Your Own Docs

Edit `setup_store.py` to point to your own markdown files:

```python
MY_DOCS = {
    "my-doc.md": "https://raw.githubusercontent.com/you/repo/main/doc.md",
}
```

### Change the Model

In `app.py`, try different models:

```python
model='gemini-2.5-pro',  # More capable, slower
model='gemini-2.5-flash',  # Faster, good balance
```

### Add System Instructions

In `app.py`, add personality to the assistant:

```python
config=types.GenerateContentConfig(
    system_instruction="You are a helpful MLH expert. Be concise and friendly.",
    tools=[file_search_tool],
    response_modalities=["TEXT"],
)
```

### Adjust Temperature

Control randomness (0 = deterministic, 1 = creative):

```python
config=types.GenerateContentConfig(
    temperature=0.3,  # More focused and consistent
    tools=[file_search_tool],
    response_modalities=["TEXT"],
)
```

## Next Steps

- Read through the code to understand how each piece works
- Check out the main [WORKSHOP.md](../docs/WORKSHOP.md) for a step-by-step tutorial
- Watch the stream recording (link in main README)
- Build your own RAG app with different docs!

## Resources

- [Gemini File Search Docs](https://ai.google.dev/gemini-api/docs/file-search)
- [Google AI Studio](https://aistudio.google.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [MLH on GitHub](https://github.com/MLH)
