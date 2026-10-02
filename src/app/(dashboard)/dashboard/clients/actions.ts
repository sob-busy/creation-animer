"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { canManage, getCurrentStudio } from "@/lib/studio";
import { createClient } from "@/lib/supabase/server";
import { clientSchema, toClientRow, uuidSchema } from "@/lib/validations/client";
import { echoValues, parseForm, type FormState } from "@/lib/validations/form";

// Every action re-checks auth (getCurrentStudio → requireUser) and relies on RLS:
// Server Actions are reachable by direct POST, not only through our UI.

export async function createClientAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const studio = await getCurrentStudio();
  const parsed = parseForm(clientSchema, formData);
  if (!parsed.data) return parsed.state;

  const supabase = await createClient();
  const { data, error } = await supabase
    .from("clients")
    .insert({ studio_id: studio.id, ...toClientRow(parsed.data) })
    .select("id")
    .single();
  if (error || !data) {
    return { error: "Impossible d'enregistrer ce client.", values: echoValues(Object.fromEntries(formData)) };
  }
  revalidatePath("/dashboard", "layout");
  redirect(`/dashboard/clients/${data.id}?created=1`);
}

export async function updateClientAction(id: string, _prev: FormState, formData: FormData): Promise<FormState> {
  await getCurrentStudio();
  if (!uuidSchema.safeParse(id).success) return { error: "Client introuvable." };
  const parsed = parseForm(clientSchema, formData);
  if (!parsed.data) return parsed.state;

  const supabase = await createClient();
  const { data, error } = await supabase.from("clients").update(toClientRow(parsed.data)).eq("id", id).select("id");
  if (error || !data?.length) {
    return { error: "Modification impossible.", values: echoValues(Object.fromEntries(formData)) };
  }
  revalidatePath("/dashboard", "layout");
  return { success: "Fiche client enregistrée." };
}

export async function deleteClientAction(id: string): Promise<FormState> {
  const studio = await getCurrentStudio();
  if (!canManage(studio)) return { error: "Seuls les administrateurs du studio peuvent supprimer un client." };
  if (!uuidSchema.safeParse(id).success) return { error: "Client introuvable." };

  const supabase = await createClient();
  const { data, error } = await supabase.from("clients").delete().eq("id", id).select("id");
  if (error?.code === "23503") {
    return { error: "Ce client a des factures : annulez-les ou conservez la fiche." };
  }
  if (error || !data?.length) return { error: "Suppression impossible." };

  revalidatePath("/dashboard", "layout");
  redirect("/dashboard/clients");
}
