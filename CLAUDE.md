# Todo App - Hackathon II

> This is a monorepo using GitHub Spec-Kit for spec-driven development.

---

## Spec-Kit Structure

Specifications are organized in `/specs`:

| Directory | Purpose |
|-----------|---------|
| `/specs/overview.md` | Project overview |
| `/specs/features/` | Feature specs (what to build) |
| `/specs/api/` | API endpoint and MCP tool specs |
| `/specs/database/` | Schema and model specs |
| `/specs/ui/` | Component and page specs |

---

## How to Use Specs

1. **Always read relevant spec before implementing**
2. Reference specs with: `@specs/features/task-crud.md`
3. Update specs if requirements change

---

## Project Structure

```
hackathon-todo/
├── .spec-kit/
│   └── config.yaml         # Spec-Kit configuration
├── specs/
│   ├── overview.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── frontend/               # Next.js 16+ app
│   └── CLAUDE.md
├── backend/                # FastAPI server
│   └── CLAUDE.md
├── CLAUDE.md               # This file
└── README.md
```

---

## Development Workflow

1. Read spec: `@specs/features/[feature].md`
2. Implement backend: `@backend/CLAUDE.md`
3. Implement frontend: `@frontend/CLAUDE.md`
4. Test and iterate

---

## Commands

```bash
# Frontend
cd frontend && npm run dev

# Backend
cd backend && uv run uvicorn src.main:app --reload

# Both (Docker)
docker-compose up
```

---

## Phase Specifications

| Phase | Spec File |
|-------|-----------|
| I | `specs/001-phase1.md` |
| II | `specs/features/task-crud.md`, `specs/features/authentication.md` |
| III | `specs/features/chatbot.md`, `specs/api/mcp-tools.md` |

---

*Spec-Kit Plus | Evolution of Todo*
