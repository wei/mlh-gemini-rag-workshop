#!/usr/bin/env python3
"""
Simple CLI tool to test RAG queries against your FileSearchStore.

Usage:
    python query_test.py <store_name> <query>

Example:
    python query_test.py "vectorstores/abc123" "How do I get reimbursed for a Hack Day?"
    
Or read store name from .env:
    python query_test.py "What are MLH's code of conduct policies?"
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
    Query the RAG system and return the response text and citations.
    
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
    
    # Create file search tool with the store
    file_search_tool = types.Tool(
        file_search=types.FileSearch(
            vector_store_names=[store_name]
        )
    )
    
    # Generate response
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=query,
        config=types.GenerateContentConfig(
            tools=[file_search_tool],
            response_modalities=["TEXT"],
        )
    )
    
    # Extract text and citations
    text = response.text
    citations = []
    
    # Extract citations from grounding metadata
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
        print("❌ Error: Missing arguments")
        print("\nUsage:")
        print("  python query_test.py <store_name> <query>")
        print("  python query_test.py <query>  (reads store from .env)")
        print("\nExample:")
        print('  python query_test.py "vectorstores/abc123" "How do I organize a hackathon?"')
        sys.exit(1)
    
    # Determine store name and query
    if len(sys.argv) == 2:
        # Read store from .env
        store_name = os.getenv("FILE_SEARCH_STORE_NAME")
        if not store_name:
            print("❌ Error: FILE_SEARCH_STORE_NAME not found in .env file")
            sys.exit(1)
        query = sys.argv[1]
    else:
        store_name = sys.argv[1]
        query = sys.argv[2]
    
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
                    # Show first 100 chars of cited text
                    preview = citation['text'][:100]
                    if len(citation['text']) > 100:
                        preview += "..."
                    print(f"   \"{preview}\"")
                print()
        else:
            print("\n(No citations found)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
