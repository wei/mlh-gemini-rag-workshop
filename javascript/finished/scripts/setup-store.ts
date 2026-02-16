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
    console.log(`  1. Copy .env.example to .env`);
    console.log(`  2. Add your GOOGLE_API_KEY`);
    console.log(`  3. Run: npm run dev`);
    
  } catch (error) {
    console.error(`\n❌ Setup failed:`, error);
    process.exit(1);
  }
}

main();
