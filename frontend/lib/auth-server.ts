/**
 * Better Auth Server Configuration
 * 
 * Reference: @specs/features/authentication.md
 * This handles user signup, login, and session management.
 */

import { betterAuth } from "better-auth";

export const auth = betterAuth({
    // Using memory adapter for demo - in production use database
    database: {
        type: "memory"
    },
    // Email and password authentication
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
    },
    // Session settings
    session: {
        expiresIn: 60 * 60 * 24 * 7, // 7 days
        updateAge: 60 * 60 * 24, // 1 day
    },
    // Secret for JWT signing
    secret: process.env.BETTER_AUTH_SECRET || "hackathon-secret-key-2024",
    // Base URL for auth callbacks
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "https://frontend-cd6l1v0dr-tasmeerjamali2004-6802s-projects.vercel.app",
});
