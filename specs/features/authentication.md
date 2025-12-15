# Feature: Authentication

> Specification for Better Auth integration with JWT tokens.

---

## User Stories

### US-AUTH-001: User Signup
**As a** new user  
**I want to** create an account with email and password  
**So that** I can access the todo application

### US-AUTH-002: User Signin
**As a** registered user  
**I want to** log in with my credentials  
**So that** I can access my tasks

### US-AUTH-003: JWT Token
**As a** logged-in user  
**I want** my session secured with a JWT token  
**So that** my data remains protected

---

## Acceptance Criteria

### AC-AUTH-001: Signup
| Criterion | Description |
|-----------|-------------|
| AC-AUTH-001.1 | Email must be valid and unique |
| AC-AUTH-001.2 | Password must be at least 8 characters |
| AC-AUTH-001.3 | Account is created and JWT issued |

### AC-AUTH-002: Signin
| Criterion | Description |
|-----------|-------------|
| AC-AUTH-002.1 | Valid credentials return JWT token |
| AC-AUTH-002.2 | Invalid credentials return 401 error |
| AC-AUTH-002.3 | Token contains user_id and email |

### AC-AUTH-003: JWT Verification
| Criterion | Description |
|-----------|-------------|
| AC-AUTH-003.1 | All API requests require `Authorization: Bearer <token>` |
| AC-AUTH-003.2 | Invalid token returns 401 Unauthorized |
| AC-AUTH-003.3 | Expired token returns 401 with "Token expired" |
| AC-AUTH-003.4 | Backend extracts user_id from token |

---

## Technical Implementation

### Better Auth (Frontend)
```typescript
// lib/auth.ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL,
});
```

### FastAPI JWT Middleware (Backend)
```python
# Extracts token from Authorization: Bearer header
# Verifies signature using BETTER_AUTH_SECRET
# Decodes user_id from token payload
```

---

*Spec-Kit Plus | Evolution of Todo*
