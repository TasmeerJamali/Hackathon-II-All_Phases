/**
 * Landing Page - Redirects to login or dashboard
 * 
 * Reference: @specs/ui/pages.md
 */

import { redirect } from "next/navigation";

export default function Home() {
    // Redirect to login (in a real app, check auth state first)
    redirect("/login");
}
