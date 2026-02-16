#!/usr/bin/env python3
"""
Setup script to create a FileSearchStore and upload MLH documentation.

This script:
1. Creates a new FileSearchStore for organizing documents
2. Downloads MLH docs from GitHub (raw markdown files)
3. Uploads them to the store
4. Polls until indexing is complete
5. Prints the store name for use in your .env file

Run this once before using the chat app:
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

# MLH documentation URLs (raw GitHub content)
MLH_DOCS = {
    "hackathon-organizer-guide.md": "https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/main/README.md",
    "mlh-policies.md": "https://raw.githubusercontent.com/MLH/mlh-policies/main/README.md",
    "code-of-conduct.md": "https://raw.githubusercontent.com/MLH/mlh-policies/main/code-of-conduct.md",
    "hack-days-guide.md": "https://raw.githubusercontent.com/MLH/mlh-hack-days-organizer-guide/main/README.md",
}


def download_file(url: str, filename: str, temp_dir: Path) -> Path:
    """Download a file from URL to temp directory."""
    print(f"  Downloading {filename}...")
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
    
    # Create FileSearchStore
    print("📦 Creating FileSearchStore...")
    store = client.vector_stores.create(
        config=types.CreateVectorStoreConfig(
            display_name="MLH Documentation Store",
        )
    )
    print(f"✅ Created store: {store.name}")
    
    # Download and upload files
    print("\n📥 Downloading and uploading MLH docs...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        for filename, url in MLH_DOCS.items():
            try:
                # Download file
                file_path = download_file(url, filename, temp_path)
                
                # Upload to Gemini Files API
                print(f"  Uploading {filename} to Gemini Files...")
                uploaded_file = client.files.upload(file=str(file_path))
                
                # Add file to vector store
                print(f"  Adding {filename} to store...")
                client.vector_stores.add_files(
                    vector_store=store.name,
                    files=[uploaded_file.name]
                )
                
                print(f"✅ {filename} uploaded and added to store\n")
                
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}\n")
    
    # Wait for indexing
    wait_for_indexing(client, store.name)
    
    # Print final instructions
    print("\n" + "="*60)
    print("🎉 Setup complete!")
    print("="*60)
    print(f"\nStore Name: {store.name}")
    print("\n📝 Next steps:")
    print("1. Copy the store name above")
    print("2. Add it to your .env file:")
    print(f"   FILE_SEARCH_STORE_NAME={store.name}")
    print("3. Run the chat app:")
    print("   streamlit run app.py")
    print("\nOr test it from the command line first:")
    print(f'   python query_test.py "{store.name}" "How do I get reimbursed for a Hack Day?"')
    print()


if __name__ == "__main__":
    main()
