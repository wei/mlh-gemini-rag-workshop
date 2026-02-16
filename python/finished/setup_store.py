#!/usr/bin/env python3
"""
Setup script to create a Gemini FileSearchStore and upload MLH documentation.

This script:
1. Creates a new FileSearchStore
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
# Note: mlh-hackathon-organizer-guide uses 'master' branch, others use 'main'
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
    """Download a file from URL to temp directory."""
    print(f"  📥 Downloading {filename}...")
    response = requests.get(url)
    response.raise_for_status()

    file_path = temp_dir / filename
    file_path.write_text(response.text, encoding="utf-8")
    print(f"     ({len(response.text)} chars)")
    return file_path


def wait_for_indexing(client: genai.Client, store_name: str, timeout: int = 300):
    """Poll the store until all documents are indexed."""
    print("\n⏳ Waiting for indexing to complete...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        store = client.file_search_stores.get(name=store_name)

        active = store.active_documents_count or 0
        pending = store.pending_documents_count or 0
        failed = store.failed_documents_count or 0
        total = active + pending + failed

        print(f"  Progress: {active} active, {pending} pending, {failed} failed (total: {total})")

        if pending == 0 and total > 0:
            if failed > 0:
                print(f"  ⚠️  {failed} documents failed to index")
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
    store = client.file_search_stores.create(
        config=types.CreateFileSearchStoreConfig(
            display_name="MLH Documentation Store",
        )
    )
    print(f"✅ Created store: {store.name}")

    # Download and upload files
    print("\n📄 Downloading and uploading MLH docs...\n")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for filename, url in MLH_DOCS.items():
            try:
                # Download file
                file_path = download_file(url, filename, temp_path)

                # Upload directly to the FileSearchStore
                print(f"  📤 Uploading {filename} to store...")
                operation = client.file_search_stores.upload_to_file_search_store(
                    file_search_store_name=store.name,
                    file=str(file_path),
                )

                # Wait for upload operation to complete
                while not operation.done:
                    time.sleep(2)
                    operation = client.operations.get(operation)

                if operation.error:
                    print(f"  ❌ Error uploading {filename}: {operation.error}")
                else:
                    print(f"  ✅ {filename} uploaded successfully\n")

            except Exception as e:
                print(f"  ❌ Error processing {filename}: {e}\n")

    # Wait for indexing
    wait_for_indexing(client, store.name)

    # Print final instructions
    print("\n" + "=" * 60)
    print("🎉 Setup complete!")
    print("=" * 60)
    print(f"\nStore Name: {store.name}")
    print("\n📝 Next steps:")
    print("1. Copy the store name above")
    print("2. Add it to your .env file:")
    print(f"   FILE_SEARCH_STORE_NAME={store.name}")
    print("3. Test from the command line:")
    print(f'   python query_test.py "How do I get reimbursed for a Hack Day?"')
    print("4. Or run the chat app:")
    print("   streamlit run app.py")
    print()


if __name__ == "__main__":
    main()
