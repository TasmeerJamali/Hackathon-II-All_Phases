# UI Components Specification

> Frontend component specifications for Next.js.

---

## Component Library

- Framework: Next.js 16+ (App Router)
- Styling: Tailwind CSS
- Icons: Lucide React

---

## Page Components

### Login Page (`/login`)
- Email input field
- Password input field
- "Sign In" button
- Link to signup page
- Better Auth integration

### Signup Page (`/signup`)
- Name input field
- Email input field
- Password input field
- "Create Account" button
- Link to login page

### Dashboard (`/dashboard`)
- Task list component
- Add task button
- Filter controls (status, priority)
- Search input
- User menu with logout

### Chat Page (`/chat`) - Phase III
- OpenAI ChatKit component
- Message history
- Input field
- Send button

---

## Reusable Components

### TaskCard
- Task title
- Status indicator (✅/❌)
- Priority badge
- Due date (if set)
- Actions: Edit, Delete, Toggle

### TaskForm
- Title input (required)
- Description textarea
- Priority select
- Due date picker
- Submit button

### Navbar
- Logo
- Navigation links
- User avatar
- Logout button

---

## Design Tokens

| Token | Value |
|-------|-------|
| Primary | #3B82F6 |
| Secondary | #111827 |
| Accent | #FACC15 |
| Background | #FFFFFF |
| Error | #EF4444 |
| Success | #22C55E |

---

*Spec-Kit Plus | Evolution of Todo*
