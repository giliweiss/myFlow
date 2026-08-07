# Architecture Revision at a Glance

## The Problem (Before)

```
mobile app
  ├─ calls Supabase for CRUD (groups, lessons, etc) ❌ scattered auth checks
  └─ calls FastAPI for filtering/validation ❌ low-level endpoints

Business logic scattered, hard to verify ownership
```

## The Solution (After)

```
mobile app
  └─ calls FastAPI for everything ✓ one place to verify ownership
       └─ FastAPI calls Supabase ✓ clean separation of concerns

All product operations go through FastAPI, which controls the flow
```

---

## Example Flow: Generate a Lesson

### Before
```
Mobile                FastAPI                  Supabase
  │                    │                         │
  ├─ POST /exercises/filter ─────────────────────┤ (no ownership check here)
  │  ← exercises list
  │
  ├─ POST /lessons/validate
  │  ← is valid?
  │
  ├─ POST /groups/{id} ──────────────────────────┤ (load group context)
  │  ← group
  │
  ├─ SELECT lesson history ──────────────────────┤ (need to check ownership manually)
  │  ← lessons
  │
  ├─ INSERT lesson ───────────────────────────────┤
```

### After
```
Mobile           FastAPI                         Supabase
  │               │                               │
  └─ POST /groups/{id}/lessons/generate          │
              │                                   │
              ├─ verify user owns group ✓        │
              │                                   │
              ├─ load group context ─────────────┤
              │                                   │
              ├─ load lesson history ────────────┤
              │                                   │
              ├─ load recent reviews ────────────┤
              │                                   │
              ├─ filter exercises (internal)     │
              │                                   │
              ├─ call LLM (internal)             │
              │                                   │
              ├─ validate result (internal)      │
              │                                   │
              ├─ save lesson ─────────────────────┤
              │                                   │
              └─ return full lesson ────────────> (user sees result)
```

---

## File Changes Summary

### Backend Added

```
app/repositories/           (NEW layer for data access)
  ├── base_repo.py         (abstract base)
  ├── group_repo.py        (groups queries)
  ├── lesson_repo.py       (lessons queries)
  ├── review_repo.py       (reviews queries)
  └── exercise_repo.py     (exercises queries)

app/services/
  └── lesson_generator.py  (NEW orchestration)
       - coordinates all services
       - single entry point for generation

app/api/routers/
  ├── health.py            (NEW simple health check)
  ├── groups.py            (NEW main groups API)
  └── lessons.py           (NEW main lessons API)
```

### Backend Removed/Hidden

```
/exercises/filter          → now internal (ExerciseFilter service)
/lessons/validate          → now internal (LessonValidator service)
/exercises/seed            → moved to scripts/seed_exercises.py
```

### Mobile Reorganized

```
src/lib/api-client.ts
  ├── groupsApi.getGroups()
  ├── groupsApi.createGroup()
  ├── lessonsApi.generateLesson()      ← High-level, orchestrated
  ├── lessonsApi.submitReview()
  └── progressApi.getGroupProgress()

       ALL endpoints are product-level operations
       NO low-level /filter or /validate calls
```

---

## Responsibility Matrix

| Who | What | Where |
|-----|------|-------|
| Mobile | Renders UI, handles user input | Expo screens |
| Mobile | Gets JWT from Supabase | supabase.auth |
| Mobile | Calls product APIs | apiClient.groups.* |
| FastAPI | Authorizes request (owns group?) | get_current_user |
| FastAPI | Loads group, history, reviews | repositories |
| FastAPI | Filters exercises | ExerciseFilter (internal) |
| FastAPI | Calls LLM | LLMService (internal) |
| FastAPI | Validates result | LessonValidator (internal) |
| FastAPI | Saves to DB | LessonRepository |
| FastAPI | Returns full lesson | HTTP response |
| Supabase | Authenticates user | auth.users |
| Supabase | Stores data | groups, lessons, etc |
| Supabase | RLS (defense in depth) | Row-level security policies |

---

## Verification Checklist

- [x] Backend starts without errors
- [x] New API endpoints defined (groups, lessons, progress)
- [x] Repository layer created and imported
- [x] LessonGeneratorService stub in place
- [x] Auth middleware updated
- [x] Mobile API client reorganized
- [x] Supabase client auth-only
- [x] All service stubs ready for Phase 1
- [x] Project structure clean and logical

---

## Ready for Phase 1

All pieces are in place. Phase 1 will implement:

1. **JWT verification** → decode Supabase tokens
2. **Repositories** → connect to Supabase
3. **LessonGeneratorService** → orchestrate full flow
4. **Router endpoints** → call services, return responses
5. **Mobile hooks** → React Query for state management

The architecture is clean, the responsibility split is clear, and the codebase is ready to scale.
