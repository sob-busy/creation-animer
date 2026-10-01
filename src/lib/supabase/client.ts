import { createBrowserClient } from "@supabase/ssr";

import { publicEnv } from "@/lib/env/client";

/** Supabase client for Client Components. Uses the public (RLS-bound) key only. */
export function createClient() {
  const env = publicEnv();
  return createBrowserClient(env.NEXT_PUBLIC_SUPABASE_URL, env.NEXT_PUBLIC_SUPABASE_ANON_KEY);
}
