/**
 * Main Chat Page
 * 
 * Uses Vercel AI SDK's useChat hook for:
 * - Managing chat state
 * - Streaming responses
 * - Form handling
 */

'use client';

import { useChat } from 'ai/react';
import { ChatMessage } from '@/components/chat-message';

// Example questions to help users get started
const EXAMPLE_QUESTIONS = [
  "What are the key responsibilities of an MLH hackathon organizer?",
  "What is the MLH Code of Conduct?",
  "How do I run an MLH Hack Day?",
  "What resources does MLH provide for hackathon organizers?",
];

export default function Home() {
  // useChat hook manages all chat state and API communication
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen bg-white dark:bg-gray-950">
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            🤖 MLH Documentation Assistant
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Ask me anything about MLH hackathons, policies, and resources
          </p>
        </div>
      </header>

      {/* Main content area */}
      <div className="flex-1 overflow-hidden flex max-w-5xl w-full mx-auto">
        {/* Chat messages */}
        <div className="flex-1 flex flex-col">
          {/* Messages container */}
          <div className="flex-1 overflow-y-auto px-6 py-6 scrollbar-thin">
            {messages.length === 0 ? (
              // Welcome screen with example questions
              <div className="h-full flex flex-col items-center justify-center">
                <div className="text-center mb-8">
                  <div className="text-6xl mb-4">👋</div>
                  <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
                    Welcome!
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    Ask me anything about MLH documentation
                  </p>
                </div>

                {/* Example questions */}
                <div className="w-full max-w-2xl">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    Try asking:
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {EXAMPLE_QUESTIONS.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => {
                          // Create a synthetic form event
                          const syntheticEvent = {
                            preventDefault: () => {},
                          } as React.FormEvent<HTMLFormElement>;
                          
                          // Set the input value and submit
                          handleInputChange({
                            target: { value: question },
                          } as React.ChangeEvent<HTMLInputElement>);
                          
                          // Submit on next tick to ensure input is set
                          setTimeout(() => handleSubmit(syntheticEvent), 0);
                        }}
                        className="text-left p-4 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors border border-gray-200 dark:border-gray-700"
                      >
                        <p className="text-sm text-gray-700 dark:text-gray-300">
                          {question}
                        </p>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              // Message list
              <div className="space-y-4">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                
                {/* Loading indicator */}
                {isLoading && messages[messages.length - 1]?.role === 'user' && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-3">
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Error display */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p className="text-sm text-red-800 dark:text-red-200">
                  ❌ Error: {error.message}
                </p>
              </div>
            )}
          </div>

          {/* Input form */}
          <div className="border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4">
            <form onSubmit={handleSubmit} className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={handleInputChange}
                placeholder="Ask a question..."
                disabled={isLoading}
                className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
