# Architecture Revision Summary

## What Changed

The application architecture has been restructured to make **FastAPI the main backend** while Supabase serves only authentication and database storage.

### Before
```
Mobile (Expo)
  ├─ Supabase JS Client → Direct CRUD (groups, lessons, etc)
  └─ FastAPI → Low-level operations (/exercises/filter, /lessons/validate)
```

### After
```
Mobile (Expo)
  └─ FastAPI → Product-level operations (groups CRUD, lesson generation, etc)
       └─ Supabase → Auth + Database
```

---

## Backend Changes

### New File Structure

**New directories/layers:**
- `app/repositories/` — Data access layer (BaseRepository, GroupRepository, LessonRepository, ReviewRepository, ExerciseRepository)
- `app/services/lesson_generator.py` — Orchestration service for lesson generation

**New routers:**
- `app/api/routers/health.py` — `GET /health`
- `app/api/routers/groups.py` — Groups CRUD + lesson operations
- `app/api/routers/lessons.py` — Lesson detail + reviews

**Updated files:**
- `app/main.py` — Removed exercises/reviews as direct routers, added proper middleware
- `app/core/auth.py` — JWT verification from Authorization header
- `app/db/session.py` — Supabase client factory

**Removed (now internal, not public endpoints):**
- `/exercises/filter` endpoint (ExerciseFilter is now an internal service)
- `/lessons/validate` endpoint (LessonValidator is now an internal service)
- `/exercises/seed` endpoint (moved to scripts/seed_exercises.py)

### New API Endpoints

**Groups**
```
GET    /groups                          → list instructor's groups
POST   /groups                          → create group
GET    /groups/{group_id}               → get group detail
PATCH  /groups/{group_id}               → update group
GET    /groups/{group_id}/lessons       → list group's lessons
POST   /groups/{group_id}/lessons/generate  → generate lesson (orchestrated)
GET    /groups/{group_id}/progress      → group progress summary
```

**Lessons**
```
GET    /lessons/{lesson_id}             → get lesson detail
PATCH  /lessons/{lesson_id}             → update lesson
POST   /lessons/{lesson_id}/exercises/{item_id}/replace  → swap exercise
POST   /lessons/{lesson_id}/review      → submit review
```

**Health**
```
GET    /health                          → {"status": "ok"}
```

### Service Architecture

**Lesson Generation Flow (Internal)**

```
POST /groups/{group_id}/lessons/generate
  ↓
LessonGeneratorService.generate()
  ├─ GroupRepository.get_by_id()
  ├─ LessonRepository.get_recent_history()
  ├─ ReviewRepository.get_recent_by_group()
  ├─ ExerciseRepository.list_all()
  ├─ ExerciseFilter.filter_exercises()  [internal service]
  ├─ LLMService.generate()              [internal service]
  ├─ LessonValidator.validate()         [internal service]
  └─ LessonRepository.create_draft()
  ↓
return lesson
```

**Authorization Pattern**

Every endpoint:
1. Gets current user from JWT (`get_current_user`)
2. Loads the resource
3. Verifies user ownership (TODO: implement ownership check)
4. Executes operation
5. Returns result

---

## Mobile Changes

### New API Client Structure

**Before:** Low-level + mixed Supabase
```typescript
apiClient.filterExercises()    // Low-level internal step
apiClient.validateLesson()     // Low-level internal step
supabase.from("groups").select() // Direct CRUD
```

**After:** Product-level operations only
```typescript
apiClient.groups.getGroups()
apiClient.groups.createGroup()
apiClient.groups.getGroup()
apiClient.groups.updateGroup()

apiClient.lessons.getGroupLessons()
apiClient.lessons.generateLesson()  // Orchestrated by backend
apiClient.lessons.getLesson()
apiClient.lessons.updateLesson()
apiClient.lessons.replaceExercise()
apiClient.lessons.submitReview()

apiClient.progress.getGroupProgress()
```

### Updated Files

**`src/lib/api-client.ts`**
- Reorganized into `groupsApi`, `lessonsApi`, `progressApi`
- All operations call product-level endpoints on FastAPI
- No `/exercises/filter` or `/lessons/validate` calls
- Returns high-level results (full lesson, group, etc)

**`src/lib/supabase.ts`**
- Now auth-only (signup, login, logout, session)
- No product CRUD
- Exports `supabase` client + `authHelpers`
- JWT tokens used for FastAPI Authorization header

---

## Responsibility Split

| Operation | Before | After |
|-----------|--------|-------|
| List groups | Mobile → Supabase | Mobile → FastAPI |
| Create group | Mobile → Supabase | Mobile → FastAPI |
| Generate lesson | Mobile → FastAPI (low-level filter/validate) | Mobile → FastAPI (orchestrated) |
| Save lesson | Mobile → Supabase | FastAPI → Supabase |
| Load lesson history | Mobile → Supabase | FastAPI → Supabase |
| Auth | Supabase | Supabase (same) |
| Exercise filtering | FastAPI (public endpoint) | FastAPI (internal service) |
| Lesson validation | FastAPI (public endpoint) | FastAPI (internal service) |

---

## What Stays the Same

- Mobile app routing structure (file-based Expo Router)
- Screen placeholder components
- Exercise data model
- Filtering & validation logic (just moved from public to internal)
- LLM service stub
- Dependencies (Expo, FastAPI, Supabase, etc)

---

## Next Steps (Phase 1)

1. **Implement JWT verification** in `app/core/auth.py`
   - Decode Supabase JWT tokens
   - Extract `sub` (user ID) / `instructor_id`

2. **Implement repositories** (data access layer)
   - Connect to Supabase using supabase-py client
   - Handle query logic

3. **Implement LessonGeneratorService**
   - Wire up all the internal services
   - Orchestrate the full generation flow
   - Validate result before saving

4. **Implement router endpoints**
   - Call repositories + services
   - Return proper responses
   - Add error handling

5. **Implement mobile hooks** (React Query / TanStack Query)
   - `useGroups()`, `useGroup(id)`, etc.
   - Handle loading, error, success states

---

## Verification

✓ Backend starts: `uv run uvicorn app.main:app --reload`
✓ Mobile builds: `cd mobile && npx expo start`
✓ New API structure in place
✓ Supabase auth-only client configured
✓ Repositories layer ready for implementation
✓ Internal services preserved (not exposed)
