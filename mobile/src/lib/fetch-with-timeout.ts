export const defaultTimeoutMs = 30_000;
export const generateLessonTimeoutMs = 120_000;

export async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeoutMs = defaultTimeoutMs,
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, {
      ...options,
      signal: controller.signal,
    });
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error(`Request timed out after ${timeoutMs}ms: ${url}`);
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}
