// Utility functions (to be populated in Phase 1)

export const formatDate = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString();
};

export const formatTime = (time: string): string => {
  // Format HH:mm
  return time;
};
