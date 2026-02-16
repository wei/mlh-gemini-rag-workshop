#!/usr/bin/env python3
"""
MLH Documentation Assistant - A RAG-powered chatbot using Gemini File Search

This Streamlit app lets you chat with MLH's documentation using RAG.
It uses Gemini's File Search feature to retrieve relevant context
and generate accurate, grounded responses with citations.
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

# Sidebar
with st.sidebar:
    st.title("🎓 MLH Doc Assistant")
    st.markdown("Ask questions about MLH's documentation!")
    
    st.divider()
    
    # Store name input
    default_store = os.getenv("FILE_SEARCH_STORE_NAME", "")
    store_name = st.text_input(
        "FileSearchStore Name",
        value=default_store,
        help="The vector store name from setup_store.py"
    )
    
    if not store_name:
        st.warning("⚠️ Please enter a store name or add it to your .env file")
    
    st.divider()
    
    # Example questions
    st.subheader("💡 Try asking:")
    example_questions = [
        "How do I get reimbursed for a Hack Day?",
        "What are the requirements to be an MLH member event?",
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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def get_gemini_client():
    """Initialize and return Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found. Add it to your .env file.")
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
    
    # Create file search tool
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
    full_response = ""
    citations = []
    
    for chunk in stream:
        if hasattr(chunk, 'text') and chunk.text:
            full_response += chunk.text
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
                        st.caption(f'"{citation["text"][:200]}..."' if len(citation['text']) > 200 else f'"{citation["text"]}"')
                    st.divider()

# Handle pending question from sidebar
if st.session_state.pending_question:
    user_input = st.session_state.pending_question
    st.session_state.pending_question = None
else:
    user_input = st.chat_input("Ask a question about MLH...")

# Process user input
if user_input:
    if not store_name:
        st.error("⚠️ Please enter a FileSearchStore name in the sidebar")
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
                            st.caption(f'"{citation["text"][:200]}..."' if len(citation['text']) > 200 else f'"{citation["text"]}"')
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
    st.info("👋 Welcome! Ask me anything about MLH's documentation. Try one of the example questions in the sidebar!")
