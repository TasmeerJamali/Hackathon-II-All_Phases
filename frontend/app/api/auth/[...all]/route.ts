/**
 * Better Auth API Route Handler
 * 
 * Catches all auth-related requests (/api/auth/*)
 * Reference: @specs/features/authentication.md
 */

import { auth } from "@/lib/auth-server";
import { toNextJsHandler } from "better-auth/next-js";

// Export handlers for all HTTP methods
export const { GET, POST } = toNextJsHandler(auth);
