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

**Technology:** Free tier (Expo, Supabase, FastAPI + Vercel). LLM generation deferred to Phase 3+.

---

## Architecture

```
Mobile (Expo/React Native + TypeScript)
  ├─ Supabase JS Client  → CRUD for groups, lessons, reviews, exercises
  └─ FastAPI Client      → Exercise filtering, lesson validation

FastAPI (Vercel / Railway)
  └─ Supabase Postgres

Supabase Auth (JWT)
```

**Key principle:** Groups are the hub. All lesson creation/viewing happens within group context. Group history, level, equipment, and considerations automatically passed as context.

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

## Project Structure

```
myFlow/
├── docs/
│   └── mvp-plan.md
│
├── mobile/
│   ├── app/                       # Expo Router (file-based)
│   │   ├── (auth)/
│   │   │   ├── login.tsx
│   │   │   └── signup.tsx
│   │   ├── (tabs)/
│   │   │   └── index.tsx          # Groups list (home)
│   │   ├── groups/
│   │   │   ├── new.tsx
│   │   │   └── [groupId]/
│   │   │       ├── index.tsx      # Group hub
│   │   │       ├── settings.tsx
│   │   │       ├── history.tsx
│   │   │       ├── progress.tsx
│   │   │       └── lessons/
│   │   │           ├── new.tsx
│   │   │           └── [lessonId]/
│   │   │               ├── index.tsx
│   │   │               └── review.tsx
│   │   └── _layout.tsx
│   ├── src/
│   │   ├── features/              # Feature modules
│   │   │   ├── auth/
│   │   │   ├── groups/
│   │   │   ├── lessons/
│   │   │   └── progress/
│   │   ├── components/
│   │   │   └── ui/
│   │   ├── lib/
│   │   │   ├── api-client.ts
│   │   │   ├── supabase.ts
│   │   │   └── utils.ts
│   │   └── types/
│   ├── app.json
│   ├── package.json
│   └── tsconfig.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routers/
│   │   │       ├── groups.py
│   │   │       ├── lessons.py
│   │   │       ├── exercises.py
│   │   │       └── reviews.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── auth.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   └── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   │   ├── exercise_filter.py
│   │   │   ├── lesson_validator.py
│   │   │   ├── llm_service.py
│   │   │   └── progress_service.py
│   │   └── data/
│   │       └── exercises.json
│   ├── scripts/
│   │   └── seed_exercises.py
│   ├── tests/
│   ├── alembic/
│   ├── pyproject.toml
│   ├── .env.example
│   └── Dockerfile
│
├── .env.example
├── .gitignore
└── README.md
```

---

## API Design

### FastAPI Endpoints

```
POST /exercises/filter
  Body: { group_id, level, available_equipment[], group_considerations[] }
  Returns: { exercises[], restrictions }
  Purpose: Get filtered exercise pool for lesson builder

POST /lessons/validate
  Body: { lesson_exercises[], requested_duration_minutes }
  Returns: { valid: bool, issues: [], total_seconds: int }
  Purpose: Validate lesson before saving

POST /exercises/seed
  Body: exercises data (CSV/JSON)
  Purpose: Seed exercise database (admin)

GET /health
```

### Supabase (Direct from Mobile, all CRUD)

Tables with full read/write:
- `instructor_profiles`, `groups`, `lessons`, `lesson_exercises`, `lesson_reviews`

Tables with read-only:
- `exercises`, `exercise_restrictions`, `exercise_relations`, `group_exercise_history` (view)

**RLS:** All tables filtered by `auth.uid()` matching `instructor_profiles.id` (cascade to groups, then to lessons via group).

---

## User Flows

### 1. Onboarding
1. Sign up (Supabase Auth)
2. Create `instructor_profiles` (display_name)
3. Redirect to Groups List (empty state)

### 2. Create Group
1. Tap "New Group"
2. Fill: name, level, studio_name, weekday, start_time, typical_duration_minutes
3. Set: goals[], available_equipment[], group_considerations[]
4. Save → `groups` row

### 3. Create Lesson (Manual)
1. Open group → "Create Lesson"
2. Pre-filled: level, duration, equipment
3. Adjust: duration, intensity_target, goals, notes
4. FastAPI `/exercises/filter` → browse exercises (hidden/flagged by restrictions)
5. Drag-and-drop into warmup/main/cooldown
6. FastAPI `/lessons/validate` → check duration
7. Save as `draft` or `planned`

### 4. Mark as Taught
1. Open lesson from history
2. Set `actual_duration_minutes` (optional)
3. For each exercise: set `completion_status` (completed/shortened/skipped)
4. Save → `status` = `taught`, `taught_at` recorded

### 5. Add Review
1. After teaching or anytime from lesson detail
2. Fill: `perceived_difficulty`, `group_response`, `goals_achieved[]`, issues, notes
3. Save → `lesson_reviews` row

### 6. View Progress
1. Open group → "Progress"
2. Show: difficulty trend, group_response pattern, goals covered, exercise exposure, completion quality

---

## MVP Scope

### In ✓
- `instructor_profiles` linked to auth.users
- Groups CRUD (+ studio, weekday, time, considerations)
- Exercises database (seeded, `exercise_restrictions`, `exercise_relations`)
- Manual lesson creation with section builder
- Lesson status: draft/planned/taught/cancelled
- Per-exercise completion tracking + actual durations
- `lesson_reviews` (post-lesson feedback)
- Group progress screen (text-based, multi-dimensional)
- `group_exercise_history` view
- BFF: Supabase CRUD + FastAPI filter/validate
- RLS from day one
- Free tier (Vercel/Supabase)

### Out ✗ (Phase 3+)
- LLM lesson generation
- Progress graphs
- Individual participant profiles
- Multi-instructor / billing
- Custom exercises by instructor
- Reformer/apparatus Pilates
- Scheduling/calendar
- Payments
- Medical tracking
- Lesson export/PDF
- Notifications

---

## Phased Development

### Phase 0: Foundation (1–2 weeks)
- Monorepo setup (`/mobile`, `/backend`, `/docs`)
- Supabase schema + RLS + exercises seed
- FastAPI on Vercel: `/health`, `/exercises/filter`, `/exercises/seed`
- Auth flow + profile creation
- Basic navigation shell

**Deliverable:** Auth works, exercises seeded, groups list (empty)

---

### Phase 1: Group & Lesson CRUD (2–3 weeks)
- Group create/edit/list/detail
- Lesson builder (exercise selector, section organizer)
- Mark as taught + completion status
- Review form
- Lesson history

**Deliverable:** End-to-end manual lesson workflow

---

### Phase 2: Progress Layer (1–2 weeks)
- `group_exercise_history` view
- Progress screen (difficulty trend, goals, exposure, completion quality)

**Deliverable:** Meaningful progress tracking

---

### Phase 3: LLM Generation (2–3 weeks) — *requires paid API*
- Migrate FastAPI to Railway/Render
- LLM integration + auto-generate endpoint
- UI: "Auto-generate" button

**Deliverable:** Auto-generated lessons from group context

---

### Phase 4: SaaS Prep (post-MVP)
- Multi-instructor auth
- RLS audit
- Progress graphs
- Export/PDF
- Notifications

---

## Environment Variables

### Frontend (.env.local)
```
EXPO_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=xxx
EXPO_PUBLIC_API_URL=https://your-project.vercel.app
```

### Backend (Vercel)
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=xxx
```

### Phase 3+ (LLM)
```
ANTHROPIC_API_KEY=xxx
CLAUDE_MODEL=claude-haiku-4-5-20251001
```

---

## Next Steps

1. Approve plan
2. Set up Supabase project
3. Create monorepo structure
4. Initialize Phase 0 (foundation)
