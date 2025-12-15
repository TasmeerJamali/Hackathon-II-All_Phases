# UI Pages Specification

> Page specifications for Next.js App Router.

---

## Page Structure

```
frontend/app/
├── layout.tsx          # Root layout with providers
├── page.tsx            # Landing page (redirect to login)
├── (auth)/
│   ├── login/
│   │   └── page.tsx    # Login page
│   └── signup/
│       └── page.tsx    # Signup page
├── (protected)/
│   ├── layout.tsx      # Auth-protected layout
│   ├── dashboard/
│   │   └── page.tsx    # Task dashboard
│   └── chat/
│       └── page.tsx    # AI chatbot (Phase III)
└── api/
    └── auth/
        └── [...all]/
            └── route.ts # Better Auth handlers
```

---

## Page Specifications

### Landing Page (`/`)
- Redirect to `/login` if not authenticated
- Redirect to `/dashboard` if authenticated

### Login Page (`/login`)
- Better Auth signin form
- Error message display
- Loading state
- Link to signup

### Dashboard (`/dashboard`)
- Protected route (requires auth)
- Fetch tasks from `/api/{user_id}/tasks`
- CRUD operations
- Real-time updates

### Chat Page (`/chat`)
- Protected route
- OpenAI ChatKit integration
- POST to `/api/{user_id}/chat`
- Conversation history

---

*Spec-Kit Plus | Evolution of Todo*
