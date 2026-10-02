import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ClientForm } from "@/components/clients/client-form";
import { CreatedToast } from "@/components/forms/created-toast";
import { DeleteButton } from "@/components/forms/delete-button";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { canManage, getCurrentStudio } from "@/lib/studio";
import { createClient } from "@/lib/supabase/server";
import { MEASUREMENTS, uuidSchema } from "@/lib/validations/client";

import { deleteClientAction, updateClientAction } from "../actions";

export const metadata: Metadata = { title: "Fiche client" };

export default async function ClientPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ created?: string }>;
}) {
  const studio = await getCurrentStudio();
  const { id } = await params;
  if (!uuidSchema.safeParse(id).success) notFound();

  const supabase = await createClient();
  const { data: client } = await supabase
    .from("clients")
    .select("id, full_name, email, phone, notes, measurements, created_at")
    .eq("id", id)
    .maybeSingle();
  if (!client) notFound();

  const m = (client.measurements ?? {}) as Record<string, number>;
  const defaults: Record<string, string | undefined> = {
    fullName: client.full_name,
    email: client.email ?? "",
    phone: client.phone ?? "",
    notes: client.notes ?? "",
    ...Object.fromEntries(MEASUREMENTS.map(({ key }) => [`m_${key}`, m[key]?.toString() ?? ""])),
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      {(await searchParams).created && <CreatedToast message="Client créé." />}
      <PageHeader
        title={client.full_name}
        description={`Client depuis le ${new Date(client.created_at).toLocaleDateString("fr-FR", { dateStyle: "long" })}`}
        back={{ href: "/dashboard/clients", label: "Clients" }}
      />
      <ClientForm action={updateClientAction.bind(null, client.id)} defaults={defaults} submitLabel="Enregistrer" />

      {canManage(studio) && (
        <Card className="border-destructive/30">
          <CardHeader>
            <CardTitle>Zone sensible</CardTitle>
            <CardDescription>La suppression est définitive. Impossible si des factures existent.</CardDescription>
          </CardHeader>
          <CardContent>
            <DeleteButton action={deleteClientAction.bind(null, client.id)} label="Supprimer ce client" />
          </CardContent>
        </Card>
      )}
    </div>
  );
}
