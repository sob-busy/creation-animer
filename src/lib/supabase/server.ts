import "server-only";

import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";

import { publicEnv } from "@/lib/env/client";

/**
 * Supabase client for Server Components, Server Actions and Route Handlers.
 * Acts as the signed-in user: every query is subject to RLS.
 * Create a new client per request — never share one across requests.
 */
export async function createClient() {
  // Read cookies first: this opts the route into dynamic rendering before env access.
  const cookieStore = await cookies();
  const env = publicEnv();

  return createServerClient(env.NEXT_PUBLIC_SUPABASE_URL, env.NEXT_PUBLIC_SUPABASE_ANON_KEY, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options));
        } catch {
          // Called from a Server Component (read-only cookies). Safe to ignore:
          // the proxy refreshes the session on every request.
        }
      },
    },
  });
}
