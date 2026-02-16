/**
 * ChatMessage component - displays a single message with citations
 */

'use client';

import { Message } from 'ai';
import { Citation } from './citation';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  // Extract citations from tool invocations
  const citations = message.toolInvocations?.flatMap((invocation) => {
    if (invocation.toolName === 'fileSearch' && invocation.state === 'result') {
      // Parse fileSearch results for citations
      const result = invocation.result;
      if (result?.chunks) {
        return result.chunks.map((chunk: any, index: number) => ({
          text: chunk.text || chunk.content,
          source: chunk.source || chunk.uri,
          index,
        }));
      }
    }
    return [];
  }) || [];

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-blue-500 text-white'
            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
        }`}
      >
        {/* Message content */}
        <div className="whitespace-pre-wrap break-words">
          {message.content}
        </div>

        {/* Loading indicator for assistant */}
        {!isUser && message.content === '' && (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        )}

        {/* Citations */}
        {!isUser && citations.length > 0 && (
          <div className="mt-4 space-y-2">
            {citations.map((citation, index) => (
              <Citation
                key={index}
                text={citation.text}
                source={citation.source}
                index={index}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
