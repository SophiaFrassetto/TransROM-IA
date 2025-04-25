/**
 * Common utility functions
 */

/**
 * Format file size to human readable format
 * @param bytes - File size in bytes
 * @returns Formatted string (e.g., "1.5 MB")
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

/**
 * Format date to locale string
 * @param date - Date string or Date object
 * @returns Formatted date string
 */
export const formatDate = (date: string | Date): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/**
 * Calculate progress percentage
 * @param current - Current value
 * @param total - Total value
 * @returns Progress percentage
 */
export const calculateProgress = (current: number, total: number): number => {
  if (total === 0) return 0;
  return Math.round((current / total) * 100);
};

/**
 * Validate file type
 * @param file - File object
 * @param allowedTypes - Array of allowed file extensions
 * @returns Boolean indicating if file type is valid
 */
export const isValidFileType = (file: File, allowedTypes: string[]): boolean => {
  const extension = file.name.split('.').pop()?.toLowerCase();
  return extension ? allowedTypes.includes(extension) : false;
};

/**
 * Truncate text with ellipsis
 * @param text - Text to truncate
 * @param maxLength - Maximum length before truncating
 * @returns Truncated text
 */
export const truncateText = (text: string, maxLength: number): string => {
  return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
}; 