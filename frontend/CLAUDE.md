# Frontend Guidelines

> Next.js 16+ (App Router) with Better Auth

---

## Stack

| Technology | Version |
|------------|---------|
| Next.js | 16+ (App Router) |
| TypeScript | 5+ |
| Tailwind CSS | 3.4+ |
| Better Auth | 1.0+ |
| Icons | Lucide React |

---

## Patterns

- Use **server components** by default
- **Client components** only when needed (interactivity, hooks)
- API calls go through `/lib/api.ts`
- Auth state via Better Auth hooks

---

## Component Structure

```
frontend/
├── app/
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Landing
│   ├── (auth)/           # Auth pages
│   └── (protected)/      # Protected pages
├── components/
│   ├── ui/               # Reusable UI
│   ├── task/             # Task components
│   └── chat/             # Chatbot (Phase III)
├── lib/
│   ├── api.ts            # API client
│   └── auth.ts           # Better Auth client
└── CLAUDE.md             # This file
```

---

## API Client

All backend calls should use the api client:

```typescript
import { api } from '@/lib/api';

// Get tasks
const tasks = await api.getTasks(userId);

// Create task
await api.createTask(userId, { title: "New task" });
```

---

## Authentication

```typescript
import { authClient } from '@/lib/auth';

// Sign in
await authClient.signIn.email({ email, password });

// Get session (includes JWT)
const session = await authClient.getSession();
```

---

## Styling

- Use Tailwind CSS classes
- No inline styles
- Follow existing component patterns
- Design tokens in `tailwind.config.ts`

---

## Reference Specs

- `@specs/ui/components.md`
- `@specs/ui/pages.md`
- `@specs/features/authentication.md`

---

*Spec-Kit Plus | Evolution of Todo*
