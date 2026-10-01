import "server-only";

import { cache } from "react";
import { redirect } from "next/navigation";

import { createClient } from "@/lib/supabase/server";

/**
 * Returns the authenticated user or redirects to /login.
 * Call it in every protected layout/page/action: the proxy is a first gate,
 * not the only one (defense in depth). getUser() checks the session with Supabase Auth.
 */
export const requireUser = cache(async () => {
  const supabase = await createClient();
  const { data, error } = await supabase.auth.getUser();
  if (error || !data.user) redirect("/login");
  return data.user;
});
