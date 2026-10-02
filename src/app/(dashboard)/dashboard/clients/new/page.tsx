import type { Metadata } from "next";

import { ClientForm } from "@/components/clients/client-form";
import { PageHeader } from "@/components/layout/page-header";
import { getCurrentStudio } from "@/lib/studio";

import { createClientAction } from "../actions";

export const metadata: Metadata = { title: "Nouveau client" };

export default async function NewClientPage() {
  await getCurrentStudio();
  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <PageHeader title="Nouveau client" back={{ href: "/dashboard/clients", label: "Clients" }} />
      <ClientForm action={createClientAction} submitLabel="Créer la fiche" />
    </div>
  );
}
