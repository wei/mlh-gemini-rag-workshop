/**
 * Citation component - displays expandable source citations
 */

'use client';

import { useState } from 'react';

interface CitationProps {
  text: string;
  source?: string;
  index: number;
}

export function Citation({ text, source, index }: CitationProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="my-2 border border-gray-300 dark:border-gray-700 rounded-lg overflow-hidden">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-2 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors flex items-center justify-between text-left"
      >
        <span className="font-medium text-sm">
          📚 Citation {index + 1}
          {source && (
            <span className="ml-2 text-xs text-gray-600 dark:text-gray-400">
              ({source})
            </span>
          )}
        </span>
        <svg
          className={`w-4 h-4 transition-transform ${
            isExpanded ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      
      {isExpanded && (
        <div className="px-4 py-3 bg-white dark:bg-gray-900 text-sm">
          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
            {text}
          </p>
        </div>
      )}
    </div>
  );
}
