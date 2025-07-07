/**
 * Common type definitions for the application
 */

import { User } from './user';

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface RomFile {
  id: string;
  name: string;
  size: number;
  path: string;
  created_at: string;
  updated_at: string;
  user_id: string;
  user?: User;
}

export interface TranslationProject {
  id: string;
  name: string;
  description?: string;
  source_language: string;
  target_language: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  rom_file_id: string;
  rom_file?: RomFile;
  user_id: string;
  user?: User;
  created_at: string;
  updated_at: string;
}

export type { User } from './user';
export * from './user';
