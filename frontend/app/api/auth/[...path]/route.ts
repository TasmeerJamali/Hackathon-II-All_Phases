/**
 * Better Auth API Route Handler
 * 
 * This catches all auth-related requests and forwards them to the backend.
 * Reference: @specs/features/authentication.md
 */

import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://135.235.248.0";

async function handler(request: NextRequest) {
    // Get the path after /api/auth/
    const pathname = request.nextUrl.pathname;
    const authPath = pathname.replace("/api/auth", "");

    // Forward to backend auth endpoint
    const backendUrl = `${BACKEND_URL}/auth${authPath}`;

    try {
        const body = request.method !== "GET" ? await request.text() : undefined;

        const response = await fetch(backendUrl, {
            method: request.method,
            headers: {
                "Content-Type": "application/json",
                ...Object.fromEntries(request.headers),
            },
            body,
        });

        const data = await response.text();

        return new NextResponse(data, {
            status: response.status,
            headers: {
                "Content-Type": response.headers.get("Content-Type") || "application/json",
            },
        });
    } catch (error) {
        console.error("Auth proxy error:", error);
        return NextResponse.json(
            { error: "Authentication service unavailable" },
            { status: 503 }
        );
    }
}

export const GET = handler;
export const POST = handler;
export const PUT = handler;
export const DELETE = handler;
export const PATCH = handler;
