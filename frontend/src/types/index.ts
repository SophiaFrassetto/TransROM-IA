/**
 * Common type definitions for the application
 */

export interface User {
  id: string;
  email: string;
  username: string;
  createdAt: string;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface RomFile {
  id: string;
  name: string;
  size: number;
  format: string;
  uploadedAt: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}

export interface TranslationProject {
  id: string;
  romId: string;
  sourceLanguage: string;
  targetLanguage: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  createdAt: string;
  updatedAt: string;
} 