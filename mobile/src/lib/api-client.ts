// Product-level API client for FastAPI backend.

import type { Exercise } from '../types/exercise';
import type {
  CreateInstructorExerciseInput,
  InstructorExercise,
  UpdateInstructorExerciseInput,
} from '../types/instructor-exercise';
import type { Group, UpdateGroupInput } from '../types/group';
import type {
  GenerateLessonRequest,
  GenerateLessonResponse,
} from '../types/lesson-generation';
import type { CreateLessonInput, Lesson, LessonSummary, UpdateLessonInput } from '../types/lesson';
import { getApiUrl } from './api-config';
import { fetchWithTimeout } from './fetch-with-timeout';

const apiUrl = getApiUrl();

export const groupsApi = {
  async getGroups(): Promise<Group[]> {
    const res = await fetch(`${apiUrl}/groups`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /groups failed: ${res.status}`);
    const data = await res.json();
    return data.groups || [];
  },

  async getGroup(groupId: string): Promise<Group> {
    const res = await fetch(`${apiUrl}/groups/${groupId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /groups/${groupId} failed: ${res.status}`);
    return res.json();
  },

  async createGroup(groupData: UpdateGroupInput & { name: string; level: Group['level'] }): Promise<Group> {
    const res = await fetch(`${apiUrl}/groups`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(groupData),
    });
    if (!res.ok) throw new Error(`POST /groups failed: ${res.status}`);
    return res.json();
  },

  async updateGroup(groupId: string, updates: UpdateGroupInput): Promise<Group> {
    const res = await fetch(`${apiUrl}/groups/${groupId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error(`PATCH /groups/${groupId} failed: ${res.status}`);
    return res.json();
  },
};

export const exercisesApi = {
  async listExercises(): Promise<Exercise[]> {
    const res = await fetch(`${apiUrl}/exercises`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /exercises failed: ${res.status}`);
    const data = await res.json();
    return data.exercises || [];
  },

  async getExercise(exerciseId: string): Promise<Exercise> {
    const res = await fetch(`${apiUrl}/exercises/${exerciseId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /exercises/${exerciseId} failed: ${res.status}`);
    return res.json();
  },
};

export const instructorExercisesApi = {
  async listExercises(): Promise<InstructorExercise[]> {
    const res = await fetch(`${apiUrl}/instructor-exercises`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /instructor-exercises failed: ${res.status}`);
    const data = await res.json();
    return data.exercises || [];
  },

  async getExercise(exerciseId: string): Promise<InstructorExercise> {
    const res = await fetch(`${apiUrl}/instructor-exercises/${exerciseId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /instructor-exercises/${exerciseId} failed: ${res.status}`);
    return res.json();
  },

  async createExercise(input: CreateInstructorExerciseInput): Promise<InstructorExercise> {
    const res = await fetch(`${apiUrl}/instructor-exercises`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    if (!res.ok) throw new Error(`POST /instructor-exercises failed: ${res.status}`);
    return res.json();
  },

  async updateExercise(
    exerciseId: string,
    input: UpdateInstructorExerciseInput,
  ): Promise<InstructorExercise> {
    const res = await fetch(`${apiUrl}/instructor-exercises/${exerciseId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    if (!res.ok) throw new Error(`PATCH /instructor-exercises/${exerciseId} failed: ${res.status}`);
    return res.json();
  },

  async archiveExercise(exerciseId: string): Promise<InstructorExercise> {
    const res = await fetch(`${apiUrl}/instructor-exercises/${exerciseId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`DELETE /instructor-exercises/${exerciseId} failed: ${res.status}`);
    return res.json();
  },
};

export const lessonsApi = {
  async createLesson(groupId: string, input: CreateLessonInput): Promise<Lesson> {
    const res = await fetch(`${apiUrl}/groups/${groupId}/lessons`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    if (!res.ok) throw new Error(`POST /groups/${groupId}/lessons failed: ${res.status}`);
    return res.json();
  },

  async getGroupLessons(groupId: string): Promise<LessonSummary[]> {
    const res = await fetch(`${apiUrl}/groups/${groupId}/lessons`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /groups/${groupId}/lessons failed: ${res.status}`);
    const data = await res.json();
    return data.lessons || [];
  },

  async generateLesson(
    groupId: string,
    input: GenerateLessonRequest,
  ): Promise<GenerateLessonResponse> {
    const res = await fetch(`${apiUrl}/groups/${groupId}/lessons/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    if (!res.ok) throw new Error(`POST /groups/${groupId}/lessons/generate failed: ${res.status}`);
    return res.json();
  },

  async getLesson(lessonId: string): Promise<Lesson> {
    const res = await fetch(`${apiUrl}/lessons/${lessonId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error(`GET /lessons/${lessonId} failed: ${res.status}`);
    return res.json();
  },

  async updateLesson(lessonId: string, updates: UpdateLessonInput): Promise<Lesson> {
    const res = await fetch(`${apiUrl}/lessons/${lessonId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error(`PATCH /lessons/${lessonId} failed: ${res.status}`);
    return res.json();
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

export const apiClient = {
  groups: groupsApi,
  exercises: exercisesApi,
  instructorExercises: instructorExercisesApi,
  lessons: lessonsApi,
  progress: progressApi,
};
