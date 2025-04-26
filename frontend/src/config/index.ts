/**
 * Application configuration and environment variables
 */

export const config = {
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    timeout: 10000,
  },
  app: {
    name: 'TransROM-IA',
    version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
  },
  auth: {
    accessTokenKey: 'accessToken',
    refreshTokenKey: 'refreshToken',
  },
  pagination: {
    defaultPageSize: 10,
    pageSizeOptions: [5, 10, 20, 50],
  },
  supportedLanguages: [
    { code: 'en', name: 'English' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'ja', name: 'Japanese' },
  ],
  supportedRomFormats: ['gba', 'gbc', 'gb', 'nes', 'snes'],
} as const;

export type SupportedLanguage = typeof config.supportedLanguages[number]['code'];
export type SupportedRomFormat = typeof config.supportedRomFormats[number]; 