# myFlow MVP Plan

## Overview

**myFlow** is a group-centered Pilates instructor app built with **Expo/React Native** (mobile) and **FastAPI** (backend).

**Core MVP features:**
1. **Group management** — Create classes with level, studio, schedule, equipment, considerations
2. **Manual lesson creation** — Instructor selects exercises, organizes into warmup/main/cooldown
3. **Lesson tracking** — Mark as taught, record actual durations, set completion status
4. **Post-lesson reviews** — Capture perceived difficulty, group response, goals achieved
5. **Group progress** — Multi-dimensional tracking (difficulty trend, goals, exercise exposure, completion quality)

**Scope:** Single instructor, manual lessons, mat Pilates only, group-level tracking (no individual participants).

**Technology:** Free tier (Expo, Supabase, FastAPI on Vercel). LLM generation deferred to Phase 3+.

---

## Architecture

### Responsibility Split

**Expo / React Native**
- UI rendering
- User interactions
- Supabase Auth (login/signup/session)
- Call FastAPI for all product operations
- No direct Supabase CRUD (except auth)

**FastAPI (Main Backend)**
- Authorization & ownership verification
- Groups CRUD
- Lessons CRUD + history
- Lesson reviews
- Progress calculations
- Exercise retrieval + filtering (internal service)
- Lesson generation orchestration (Phase 3)
- LLM integration (Phase 3)
- Validation (internal service)

**Supabase**
- JWT Authentication
- PostgreSQL storage
- RLS policies (defense in depth)

### Data Flow

```
Mobile (Expo)
  │ (product-level API calls + Authorization header)
  └─ FastAPI
       ├─ verify JWT, load group, check ownership
       ├─ business logic (filter, validate, save)
       └─ Supabase (auth + database)
```

---

## API Design

### Group Endpoints
```
GET    /groups                          → list instructor's groups
POST   /groups                          → create group
GET    /groups/{group_id}               → get group detail
PATCH  /groups/{group_id}               → update group

GET    /groups/{group_id}/lessons       → list group's lessons
POST   /groups/{group_id}/lessons/generate  → generate lesson (Phase 3+)

GET    /groups/{group_id}/progress      → get group progress summary
```

### Lesson Endpoints
```
GET    /lessons/{lesson_id}             → get lesson detail
PATCH  /lessons/{lesson_id}             → update lesson (status, etc)

POST   /lessons/{lesson_id}/exercises/{item_id}/replace  → swap exercise in lesson
POST   /lessons/{lesson_id}/review      → submit post-lesson review
```

### Health Check
```
GET    /health → {"status": "ok"}
```

---

## Data Model

### Identity
```
auth.users (Supabase managed)
  ↓ 1:1
instructor_profiles (id, display_name, created_at, updated_at)
```

### Groups & Lessons
```
groups
  id, instructor_id, name, level (beginner/intermediate/advanced)
  studio_name, location_notes, weekday, start_time, typical_duration_minutes
  goals[], available_equipment[], group_considerations[], is_active

lessons
  id, group_id, title, status (draft/planned/taught/cancelled)
  scheduled_for, requested_duration_minutes, planned_duration_minutes, actual_duration_minutes
  intensity_target (1-5), goals[], generation_params (Phase 3+), generated_at, taught_at

lesson_exercises
  id, lesson_id, exercise_id, order_index, section (warmup/main/cooldown)
  planned_duration_seconds, actual_duration_seconds, sets, reps
  instructor_notes, placement_reason, selected_modification
  completion_status (completed/shortened/skipped), exercise_snapshot (denormalized)

lesson_reviews
  id, lesson_id, perceived_difficulty (1-5)
  group_response (too_easy/appropriate/too_hard/mixed)
  goals_achieved[], issues, instructor_notes, created_at
```

### Exercises (Curated)
```
exercises
  id, name, description, difficulty_level
  body_focus[], body_position, equipment_required[], intensity (1-5)
  min_duration_seconds, max_duration_seconds, min_reps, max_reps
  allowed_phases[], teaching_cues[], common_mistakes[]
  tags[], pilates_principles[], is_active

exercise_restrictions
  id, exercise_id, restriction_key (e.g., "lower_back")
  compatibility (allowed/modify/avoid)
  modification_notes, reference_notes

exercise_relations
  id, exercise_id, related_exercise_id
  relation_type (progression/regression/alternative)
  notes
```

### View
```
group_exercise_history (aggregated from taught lessons)
  group_id, exercise_id, times_taught, last_taught, first_taught
  times_completed, times_shortened, times_skipped
```

---

## Mobile API Client

**Product-level operations only** (no internal `/filter` or `/validate` calls):

```typescript
// Groups
apiClient.groups.getGroups(): Group[]
apiClient.groups.getGroup(id: string): Group
apiClient.groups.createGroup(data: CreateGroupInput): Group
apiClient.groups.updateGroup(id: string, data: UpdateGroupInput): Group

// Lessons
apiClient.lessons.getGroupLessons(groupId: string): Lesson[]
apiClient.lessons.generateLesson(groupId: string, params: GenerateLessonParams): Lesson
apiClient.lessons.getLesson(id: string): Lesson
apiClient.lessons.updateLesson(id: string, data: UpdateLessonInput): Lesson

// Lesson editing
apiClient.lessons.replaceExercise(lessonId: string, itemId: string, newExerciseId: string): Lesson
apiClient.lessons.submitReview(lessonId: string, review: ReviewInput): Review

// Progress
apiClient.progress.getGroupProgress(groupId: string): ProgressSummary
```

---

## Project Structure

### Backend
```
backend/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routers/
│   │       ├── health.py       # GET /health
│   │       ├── groups.py       # Groups CRUD + lessons
│   │       └── lessons.py      # Lesson detail + reviews
│   ├── core/
│   │   ├── config.py           # Settings
│   │   └── auth.py             # JWT verification
│   ├── db/
│   │   ├── session.py          # Supabase client factory
│   │   └── models.py           # Data models
│   ├── repositories/           # Data access layer
│   │   ├── base_repo.py
│   │   ├── group_repo.py
│   │   ├── lesson_repo.py
│   │   ├── review_repo.py
│   │   └── exercise_repo.py
│   ├── services/               # Business logic
│   │   ├── exercise_filter.py       # Deterministic filtering
│   │   ├── lesson_validator.py      # Validation
│   │   ├── llm_service.py           # LLM (Phase 3)
│   │   ├── lesson_generator.py      # Orchestration
│   │   └── progress_service.py      # Progress calculations
│   ├── schemas/                # Pydantic models
│   │   ├── group.py
│   │   ├── lesson.py
│   │   ├── review.py
│   │   └── exercise.py
│   └── data/
│       └── exercises.json
├── tests/
├── scripts/
├── pyproject.toml
└── Dockerfile
```

### Mobile
```
mobile/
├── app/                        # Expo Router (file-based)
│   ├── (auth)/
│   ├── (tabs)/
│   ├── groups/
│   └── _layout.tsx
├── src/
│   ├── features/              # Feature modules
│   │   ├── auth/
│   │   ├── groups/
│   │   ├── lessons/
│   │   └── progress/
│   ├── components/
│   │   └── ui/
│   ├── lib/
│   │   ├── api-client.ts      # Product-level API
│   │   ├── supabase.ts        # Auth-only client
│   │   └── utils.ts
│   └── types/
│       └── database.types.ts
└── package.json
```

---

## User Flows

### 1. Onboarding
1. Sign up (Supabase Auth)
2. Create `instructor_profiles` (display_name)
3. Redirect to Groups List

### 2. Create Group
1. Tap "New Group"
2. Fill: name, level, studio_name, weekday, start_time, typical_duration_minutes
3. Set: goals[], available_equipment[], group_considerations[]
4. Save → FastAPI POST /groups → Supabase

### 3. Create Lesson (Manual)
1. Open group → "Create Lesson"
2. Pre-filled: level, duration, equipment
3. Adjust: duration, intensity_target, goals, notes
4. Browse exercises (filtered by FastAPI `/exercises/filter` internally)
5. Drag into warmup/main/cooldown sections
6. Validate (FastAPI internal validation)
7. Save as `draft` or `planned`

### 4. Mark as Taught
1. Open lesson from history
2. Set `actual_duration_minutes` (optional)
3. For each exercise: set `completion_status`
4. Save → PATCH /lessons/{id} → `status` = `taught`

### 5. Add Review
1. After teaching (or anytime from lesson detail)
2. Fill: `perceived_difficulty`, `group_response`, `goals_achieved[]`, issues, notes
3. Save → POST /lessons/{id}/review

### 6. View Progress
1. Open group → "Progress"
2. Show: difficulty trend, group_response pattern, goals, exercise exposure, completion quality

---

## MVP Scope

### In ✓
- `instructor_profiles` linked to auth.users
- Groups CRUD (+ studio, weekday, time, considerations)
- Exercises database (seeded)
  - `exercise_restrictions` (structured)
  - `exercise_relations` (progressions/regressions)
- Manual lesson creation with section builder
- Lesson status tracking (draft → planned → taught → cancelled)
- Per-exercise completion tracking
- `lesson_reviews` (post-lesson feedback)
- Group progress screen (text-based, multi-dimensional)
- `group_exercise_history` view
- FastAPI as main backend
- Supabase auth + database only
- Authorization on all endpoints
- RLS from day one

### Out ✗ (Phase 3+)
- LLM lesson generation
- Progress graphs
- Individual participant profiles
- Multi-instructor / billing
- Custom exercises by instructor
- Reformer / apparatus Pilates
- Scheduling / calendar management
- Payments
- Medical tracking
- Lesson export / PDF
- Notifications

---

## Phased Development

### Phase 1: Group & Lesson CRUD (2–3 weeks)
- Implement JWT verification
- Implement repositories (Supabase queries)
- Implement router endpoints
- Group create/edit/list/detail
- Lesson builder (exercise selector, section organizer)
- Mark as taught + completion status
- Review form
- Lesson history

**Deliverable:** End-to-end manual lesson workflow

### Phase 2: Progress Layer (1–2 weeks)
- `group_exercise_history` view
- Progress screen (difficulty trend, goals, exposure, completion quality)

**Deliverable:** Meaningful progress tracking

### Phase 3: LLM Generation (2–3 weeks) — *requires paid API*
- Migrate FastAPI to Railway/Render (longer timeout)
- LLM integration + auto-generate endpoint
- UI: "Auto-generate" button

**Deliverable:** Auto-generated lessons from group context

### Phase 4: SaaS Prep (post-MVP)
- Multi-instructor auth
- RLS audit
- Progress graphs
- Export/PDF
- Notifications

---

## Environment Setup

### Backend .env
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=xxx
ANTHROPIC_API_KEY=  (Phase 3+)
CLAUDE_MODEL=claude-haiku-4-5-20251001
```

### Mobile .env.local
```
EXPO_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=xxx
EXPO_PUBLIC_API_URL=http://localhost:8000
```

---

## Next Steps

1. Implement JWT verification in `app/core/auth.py`
2. Implement repositories (Supabase queries)
3. Implement router endpoints (call repositories + services)
4. Seed exercise database
5. Implement mobile hooks (React Query)
6. End-to-end test: create group → create lesson → mark taught → view progress
