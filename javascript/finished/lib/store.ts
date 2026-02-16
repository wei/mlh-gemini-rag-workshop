/**
 * Shared FileSearchStore configuration
 */

// Get store name from environment variable
export const STORE_NAME = process.env.FILE_SEARCH_STORE_NAME || 'mlh-docs-store';

// MLH documentation URLs (raw markdown from GitHub)
export const MLH_DOCS = [
  {
    name: 'mlh-hackathon-organizer-guide',
    url: 'https://raw.githubusercontent.com/MLH/mlh-hackathon-organizer-guide/main/README.md',
  },
  {
    name: 'mlh-policies',
    url: 'https://raw.githubusercontent.com/MLH/mlh-policies/main/README.md',
  },
  {
    name: 'mlh-code-of-conduct',
    url: 'https://raw.githubusercontent.com/MLH/mlh-policies/main/code-of-conduct.md',
  },
  {
    name: 'mlh-community-values',
    url: 'https://raw.githubusercontent.com/MLH/mlh-policies/main/community-values.md',
  },
  {
    name: 'mlh-hack-days-guide',
    url: 'https://raw.githubusercontent.com/MLH/mlh-hack-days-organizer-guide/main/README.md',
  },
];
