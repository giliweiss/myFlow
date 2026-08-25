export async function readApiErrorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json();
    const detail = data?.detail;

    if (typeof detail === 'string') {
      return detail;
    }

    if (detail?.message && Array.isArray(detail.issues)) {
      return `${detail.message}: ${detail.issues.join(', ')}`;
    }

    if (Array.isArray(detail)) {
      return detail.map((item) => item.msg || JSON.stringify(item)).join(', ');
    }
  } catch {
    // Fall through to status-based message.
  }

  return `Request failed: ${response.status}`;
}

export function formatLessonSaveError(message: string): string {
  if (message.includes('Exercises not suitable for this group')) {
    return 'אחד או יותר מהתרגילים שנבחרו לא מתאימים לקבוצה (רמה או ציוד). בחר/י תרגילים מהרשימה המסוננת.';
  }

  if (message.includes('Unknown exercise ids')) {
    return 'אחד מהתרגילים שנבחרו לא נמצא בקטלוג. נסה/י לבחור תרגילים מחדש.';
  }

  if (message.includes('Lesson validation failed')) {
    return message;
  }

  return message;
}
