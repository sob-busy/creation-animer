import "server-only";

import { createClient } from "@supabase/supabase-js";

import { publicEnv } from "@/lib/env/client";
import { serverEnv } from "@/lib/env/server";

/**
 * Service-role client: BYPASSES Row Level Security.
 * Only for trusted server code with no user session (e.g. verified webhooks).
 * Never use it to serve data to a user request — use lib/supabase/server instead.
 */
export function createAdminClient() {
  return createClient(publicEnv().NEXT_PUBLIC_SUPABASE_URL, serverEnv("SUPABASE_SERVICE_ROLE_KEY"), {
    auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false },
  });
}
