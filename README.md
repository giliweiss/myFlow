# myFlow

A group-centered Pilates instructor app for lesson planning, tracking, and progress analysis.

**Architecture**: FastAPI is the main backend. Supabase provides authentication and PostgreSQL storage.

## Project Structure

```
myFlow/
├── mobile/       # Expo / React Native + TypeScript frontend
├── backend/      # FastAPI backend (main API)
└── docs/         # Documentation & plans
```

## How It Works

### User Flow
1. Sign up / login via Supabase Auth
2. Call FastAPI endpoints for all product operations (groups, lessons, progress)
3. FastAPI handles authorization, orchestrates business logic, saves to Supabase

### Architecture

```
Mobile (Expo/React Native)
  │ (product-level API calls)
  └─ FastAPI (main backend)
       │ (authorization, business logic)
       └─ Supabase (auth + PostgreSQL)
```

## Development

### Backend

```bash
cd backend

# Install dependencies
uv sync

# Run development server
uv run uvicorn app.main:app --reload

# Server starts at http://localhost:8000
# Health check: GET http://localhost:8000/health
```

**Key endpoints:**
- `GET /groups` — list instructor's groups
- `POST /groups` — create group
- `POST /groups/{group_id}/lessons/generate` — generate lesson (orchestrated)
- `GET /lessons/{lesson_id}` — get lesson
- `POST /lessons/{lesson_id}/review` — submit review
- `GET /groups/{group_id}/progress` — get progress summary

See `ARCHITECTURE_CHANGES.md` for full API documentation.

### Mobile

```bash
cd mobile

# Install dependencies (already done via create-expo-app + expo install)
npm install

# Run development server
npx expo start

# Open in Expo Go app or simulator
```

**Key API client methods:**
- `apiClient.groups.getGroups()`
- `apiClient.groups.createGroup(data)`
- `apiClient.lessons.generateLesson(groupId, params)`
- `apiClient.progress.getGroupProgress(groupId)`

See `mobile/src/lib/api-client.ts` for full API client.

## Environment Setup

1. **Root .env**
   ```
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_SERVICE_KEY=xxx
   ```

2. **Backend .env** (copy from backend/.env.example)
   ```
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_SERVICE_KEY=xxx
   ANTHROPIC_API_KEY=  (Phase 3+)
   CLAUDE_MODEL=claude-haiku-4-5-20251001
   ```

3. **Mobile .env.local** (copy from mobile/.env.local)
   ```
   EXPO_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
   EXPO_PUBLIC_SUPABASE_ANON_KEY=xxx
   EXPO_PUBLIC_API_URL=http://localhost:8000
   ```

## Phased Development

- **Phase 0**: ✓ Monorepo structure (completed)
- **Phase 0.5**: ✓ Architecture revision to FastAPI-main backend (completed)
- **Phase 1**: Group & lesson CRUD + Supabase integration
- **Phase 2**: Progress tracking
- **Phase 3**: LLM lesson generation (requires paid API key)
- **Phase 4**: SaaS prep (multi-tenant, graphs, export)

## Documentation

- `docs/mvp-plan.md` — MVP scope and feature plan
- `ARCHITECTURE_CHANGES.md` — Detailed architecture revision
- `CHANGES_AT_A_GLANCE.md` — Visual before/after guide

## Key Technologies

- **Frontend**: Expo, React Native, TypeScript, TanStack Query
- **Backend**: FastAPI, Python, Pydantic
- **Database**: Supabase (PostgreSQL + Auth)
- **LLM** (Phase 3+): Claude (Anthropic)
