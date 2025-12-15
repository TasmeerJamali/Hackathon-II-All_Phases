/**
 * Better Auth Client Configuration
 * 
 * Reference: @specs/features/authentication.md
 * Reference: @frontend/CLAUDE.md
 */

import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
    baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});

// Export hooks for use in components
export const {
    useSession,
    signIn,
    signUp,
    signOut,
} = authClient;
