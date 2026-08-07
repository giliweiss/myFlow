"""Product-level API client for FastAPI backend.

Exposes high-level operations:
- Groups CRUD
- Lesson generation (orchestrated)
- Lesson operations
- Reviews
- Progress

Does NOT expose internal endpoints like /exercises/filter or /lessons/validate.
"""

const apiUrl = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Groups API
 */
export const groupsApi = {
  async getGroups(): Promise<any[]> {
    const res = await fetch(`${apiUrl}/groups`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /groups failed: ${res.status}`);
    const data = await res.json();
    return data.groups || [];
  },

  async getGroup(groupId: string): Promise<any> {
    const res = await fetch(`${apiUrl}/groups/${groupId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /groups/${groupId} failed: ${res.status}`);
    const data = await res.json();
    return data.group || {};
  },

  async createGroup(groupData: any): Promise<any> {
    const res = await fetch(`${apiUrl}/groups`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(groupData),
    });
    if (!res.ok) throw new Error(`POST /groups failed: ${res.status}`);
    const data = await res.json();
    return data.group || {};
  },

  async updateGroup(groupId: string, updates: any): Promise<any> {
    const res = await fetch(`${apiUrl}/groups/${groupId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error(`PATCH /groups/${groupId} failed: ${res.status}`);
    const data = await res.json();
    return data.group || {};
  },
};

/**
 * Lessons API
 */
export const lessonsApi = {
  async getGroupLessons(groupId: string): Promise<any[]> {
    const res = await fetch(`${apiUrl}/groups/${groupId}/lessons`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /groups/${groupId}/lessons failed: ${res.status}`);
    const data = await res.json();
    return data.lessons || [];
  },

  async generateLesson(groupId: string, params: any): Promise<any> {
    const res = await fetch(`${apiUrl}/groups/${groupId}/lessons/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) throw new Error(`POST /groups/${groupId}/lessons/generate failed: ${res.status}`);
    const data = await res.json();
    return data.lesson || {};
  },

  async getLesson(lessonId: string): Promise<any> {
    const res = await fetch(`${apiUrl}/lessons/${lessonId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /lessons/${lessonId} failed: ${res.status}`);
    const data = await res.json();
    return data.lesson || {};
  },

  async updateLesson(lessonId: string, updates: any): Promise<any> {
    const res = await fetch(`${apiUrl}/lessons/${lessonId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error(`PATCH /lessons/${lessonId} failed: ${res.status}`);
    const data = await res.json();
    return data.lesson || {};
  },

  async replaceExercise(lessonId: string, itemId: string, newExerciseId: string): Promise<any> {
    const res = await fetch(`${apiUrl}/lessons/${lessonId}/exercises/${itemId}/replace`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_exercise_id: newExerciseId }),
    });
    if (!res.ok) throw new Error(`POST /lessons/${lessonId}/exercises/${itemId}/replace failed: ${res.status}`);
    const data = await res.json();
    return data.lesson || {};
  },

  async submitReview(lessonId: string, review: any): Promise<any> {
    const res = await fetch(`${apiUrl}/lessons/${lessonId}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(review),
    });
    if (!res.ok) throw new Error(`POST /lessons/${lessonId}/review failed: ${res.status}`);
    const data = await res.json();
    return data.review || {};
  },
};

/**
 * Progress API
 */
export const progressApi = {
  async getGroupProgress(groupId: string): Promise<any> {
    const res = await fetch(`${apiUrl}/groups/${groupId}/progress`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /groups/${groupId}/progress failed: ${res.status}`);
    const data = await res.json();
    return data.progress || {};
  },
};

/**
 * Convenience client that combines all APIs
 */
export const apiClient = {
  groups: groupsApi,
  lessons: lessonsApi,
  progress: progressApi,
};
