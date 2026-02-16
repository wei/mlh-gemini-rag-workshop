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
