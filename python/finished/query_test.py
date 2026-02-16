#!/usr/bin/env python3
"""
Simple CLI tool to test RAG queries against your FileSearchStore.

Usage:
    python query_test.py <query>              (reads store name from .env)
    python query_test.py <store_name> <query>

Example:
    python query_test.py "How do I get reimbursed for a Hack Day?"
    python query_test.py "fileSearchStores/abc123" "What is the MLH code of conduct?"
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()


def query_rag(store_name: str, query: str) -> str:
    """
    Query the RAG system and return the response.

    Args:
        store_name: The FileSearchStore name (e.g., "fileSearchStores/abc123")
        query: The user's question

    Returns:
        The model's response text
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")

    client = genai.Client(api_key=api_key)

    # Create file search tool pointing to our store
    file_search_tool = types.Tool(
        file_search=types.FileSearch(
            file_search_store_names=[store_name]
        )
    )

    # Generate response using the file search tool
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config=types.GenerateContentConfig(
            tools=[file_search_tool],
        ),
    )

    return response


def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("❌ Error: Missing arguments")
        print("\nUsage:")
        print('  python query_test.py "Your question here"')
        print('  python query_test.py "fileSearchStores/abc" "Your question"')
        sys.exit(1)

    # Determine store name and query
    if len(sys.argv) == 2:
        store_name = os.getenv("FILE_SEARCH_STORE_NAME")
        if not store_name:
            print("❌ Error: FILE_SEARCH_STORE_NAME not found in .env file")
            print("   Run setup_store.py first, then add the store name to .env")
            sys.exit(1)
        query = sys.argv[1]
    else:
        store_name = sys.argv[1]
        query = sys.argv[2]

    # Execute query
    print(f"🔍 Query: {query}")
    print(f"📚 Store: {store_name}")
    print("\n" + "=" * 60 + "\n")

    try:
        response = query_rag(store_name, query)

        # Print response text
        print("💬 Response:\n")
        print(response.text)

        # Print grounding metadata if available
        if response.candidates:
            candidate = response.candidates[0]
            grounding = getattr(candidate, "grounding_metadata", None)
            if grounding:
                chunks = getattr(grounding, "grounding_chunks", None)
                if chunks:
                    print("\n" + "=" * 60)
                    print(f"📎 Sources ({len(chunks)} chunks retrieved):\n")
                    for i, chunk in enumerate(chunks, 1):
                        retrieved_context = getattr(chunk, "retrieved_context", None)
                        if retrieved_context:
                            title = getattr(retrieved_context, "title", "Unknown")
                            uri = getattr(retrieved_context, "uri", "")
                            print(f"  {i}. {title}")
                            if uri:
                                print(f"     URI: {uri}")
                        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
