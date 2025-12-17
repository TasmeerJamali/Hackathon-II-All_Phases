/**
 * Simple Auth API Route for Hackathon Demo
 * 
 * This handles signup/login for Vercel serverless deployment.
 * Uses jose for JWT signing (compatible with Edge runtime).
 */

import { NextRequest, NextResponse } from "next/server";
import { SignJWT, jwtVerify } from "jose";

const AUTH_SECRET = process.env.BETTER_AUTH_SECRET || "hackathon-secret-key-2024";
const SECRET_KEY = new TextEncoder().encode(AUTH_SECRET);

// In-memory user store (for demo - will reset on cold start)
// This is fine for hackathon demo purposes
const users: Map<string, { id: string; email: string; name: string; password: string }> = new Map();

async function signToken(payload: { sub: string; email: string; name: string }): Promise<string> {
    return new SignJWT(payload)
        .setProtectedHeader({ alg: "HS256" })
        .setIssuedAt()
        .setExpirationTime("7d")
        .sign(SECRET_KEY);
}

async function verifyToken(token: string) {
    try {
        const { payload } = await jwtVerify(token, SECRET_KEY);
        return payload as { sub: string; email: string; name: string };
    } catch {
        return null;
    }
}

export async function POST(request: NextRequest) {
    const pathname = request.nextUrl.pathname;

    try {
        const body = await request.json();

        // Handle signup - both /sign-up and /signup
        if (pathname.includes("/sign-up") || pathname.includes("/signup")) {
            const { email, password, name } = body;

            if (!email || !password) {
                return NextResponse.json(
                    { error: "Email and password required" },
                    { status: 400 }
                );
            }

            // Check if user exists
            if (users.has(email)) {
                return NextResponse.json(
                    { error: "User already exists" },
                    { status: 400 }
                );
            }

            // Create user
            const userId = `user_${Date.now()}`;
            users.set(email, { id: userId, email, name: name || email, password });

            // Generate JWT
            const token = await signToken({ sub: userId, email, name: name || email });

            return NextResponse.json({
                user: { id: userId, email, name: name || email },
                token,
                session: { token },
            });
        }

        // Handle signin - various path patterns
        if (pathname.includes("/sign-in") || pathname.includes("/signin") || pathname.includes("/login")) {
            const { email, password } = body;

            if (!email || !password) {
                return NextResponse.json(
                    { error: "Email and password required" },
                    { status: 400 }
                );
            }

            const user = users.get(email);

            if (!user || user.password !== password) {
                return NextResponse.json(
                    { error: "Invalid credentials" },
                    { status: 401 }
                );
            }

            // Generate JWT
            const token = await signToken({ sub: user.id, email: user.email, name: user.name });

            return NextResponse.json({
                user: { id: user.id, email: user.email, name: user.name },
                token,
                session: { token },
            });
        }

        // Handle session check
        if (pathname.includes("/session") || pathname.includes("/get-session")) {
            const authHeader = request.headers.get("authorization");

            if (!authHeader) {
                return NextResponse.json({ session: null });
            }

            const token = authHeader.replace("Bearer ", "");
            const decoded = await verifyToken(token);

            if (!decoded) {
                return NextResponse.json({ session: null });
            }

            return NextResponse.json({
                session: {
                    user: { id: decoded.sub, email: decoded.email, name: decoded.name },
                },
            });
        }

        // Default handler
        return NextResponse.json({ error: "Unknown auth endpoint" }, { status: 404 });

    } catch (error) {
        console.error("Auth error:", error);
        return NextResponse.json(
            { error: "Authentication failed" },
            { status: 500 }
        );
    }
}

export async function GET(request: NextRequest) {
    const pathname = request.nextUrl.pathname;

    // Handle session check
    if (pathname.includes("/session") || pathname.includes("/get-session")) {
        const authHeader = request.headers.get("authorization");

        if (!authHeader) {
            return NextResponse.json({ session: null });
        }

        const token = authHeader.replace("Bearer ", "");
        const decoded = await verifyToken(token);

        if (!decoded) {
            return NextResponse.json({ session: null });
        }

        return NextResponse.json({
            session: {
                user: { id: decoded.sub, email: decoded.email, name: decoded.name },
            },
        });
    }

    return NextResponse.json({ status: "ok" });
}
