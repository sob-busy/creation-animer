"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { canManage, getCurrentStudio } from "@/lib/studio";
import { createClient } from "@/lib/supabase/server";
import { uuidSchema } from "@/lib/validations/client";
import { echoValues, parseForm, type FormState } from "@/lib/validations/form";
import { invoiceSchema, statusSchema, TRANSITIONS } from "@/lib/validations/invoice";

export async function createInvoiceAction(_prev: FormState, formData: FormData): Promise<FormState> {
  await getCurrentStudio();
  const parsed = parseForm(invoiceSchema, formData);
  if (!parsed.data) return { ...parsed.state, values: echoValues(Object.fromEntries(formData)) };
  const d = parsed.data;

  const supabase = await createClient();
  // Totals and invoice number are computed in the database (create_invoice + triggers).
  const { data: id, error } = await supabase.rpc("create_invoice", {
    p_client_id: d.clientId,
    p_currency: d.currency,
    p_items: d.items,
    p_tax_rate_bp: d.taxRate,
    p_issued_at: d.issuedAt,
    p_due_at: d.dueAt,
    p_notes: d.notes,
  });
  if (error || !id) {
    const message = error?.message === "client_not_found" ? "Client introuvable." : "Impossible de créer la facture.";
    return { error: message, values: echoValues(Object.fromEntries(formData)) };
  }
  revalidatePath("/dashboard", "layout");
  redirect(`/dashboard/invoices/${id}?created=1`);
}

export async function setInvoiceStatusAction(id: string, next: string): Promise<FormState> {
  await getCurrentStudio();
  const status = statusSchema.safeParse(next);
  if (!uuidSchema.safeParse(id).success || !status.success) return { error: "Action invalide." };

  const supabase = await createClient();
  const { data: invoice } = await supabase.from("invoices").select("status").eq("id", id).maybeSingle();
  if (!invoice) return { error: "Facture introuvable." };
  if (!TRANSITIONS[invoice.status]?.includes(status.data)) {
    return { error: "Ce changement de statut n'est pas autorisé." };
  }

  // Optimistic concurrency: only update if the status did not change meanwhile.
  const { data, error } = await supabase
    .from("invoices")
    .update({ status: status.data })
    .eq("id", id)
    .eq("status", invoice.status)
    .select("id");
  if (error || !data?.length) return { error: "La facture a été modifiée entre-temps. Rechargez la page." };

  revalidatePath("/dashboard", "layout");
  return { success: "Statut mis à jour." };
}

export async function deleteInvoiceAction(id: string): Promise<FormState> {
  const studio = await getCurrentStudio();
  if (!canManage(studio)) return { error: "Seuls les administrateurs peuvent supprimer une facture." };
  if (!uuidSchema.safeParse(id).success) return { error: "Facture introuvable." };

  const supabase = await createClient();
  // Only drafts can be deleted; issued invoices must be voided to keep numbering intact.
  const { data, error } = await supabase.from("invoices").delete().eq("id", id).eq("status", "draft").select("id");
  if (error || !data?.length) return { error: "Seuls les brouillons peuvent être supprimés." };

  revalidatePath("/dashboard", "layout");
  redirect("/dashboard/invoices");
}
