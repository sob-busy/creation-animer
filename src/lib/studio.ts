import "server-only";

import { cache } from "react";

import { requireUser } from "@/lib/auth";
import { createClient } from "@/lib/supabase/server";

export type Studio = { id: string; name: string; default_currency: string; role: "owner" | "admin" | "member" };

/**
 * The studio the user works in (their first membership).
 * Resolved server-side and through RLS — never taken from client input.
 */
export const getCurrentStudio = cache(async (): Promise<Studio> => {
  const user = await requireUser();
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("studio_members")
    .select("role, created_at, studios!inner(id, name, default_currency)")
    .eq("user_id", user.id)
    .order("created_at", { ascending: true })
    .limit(1)
    .maybeSingle();

  if (error || !data) throw new Error("Aucun studio associé à ce compte.");
  const studio = data.studios as unknown as Omit<Studio, "role">;
  return { ...studio, role: data.role as Studio["role"] };
});

export const canManage = (studio: Studio) => studio.role === "owner" || studio.role === "admin";
