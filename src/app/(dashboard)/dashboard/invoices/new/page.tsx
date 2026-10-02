import type { Metadata } from "next";
import Link from "next/link";
import { Users } from "lucide-react";

import { InvoiceForm } from "@/components/invoices/invoice-form";
import { EmptyState } from "@/components/layout/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { getCurrentStudio } from "@/lib/studio";
import { createClient } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Nouvelle facture" };

export default async function NewInvoicePage({ searchParams }: { searchParams: Promise<{ client?: string }> }) {
  const studio = await getCurrentStudio();
  const supabase = await createClient();
  const { data: clients } = await supabase.from("clients").select("id, full_name").order("full_name").limit(500);
  const { client } = await searchParams;

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <PageHeader title="Nouvelle facture" back={{ href: "/dashboard/invoices", label: "Factures" }} />
      {!clients?.length ? (
        <EmptyState
          icon={Users}
          title="Ajoutez d'abord un client"
          text="Une facture est toujours rattachée à un client."
          action={
            <Button asChild>
              <Link href="/dashboard/clients/new">Créer un client</Link>
            </Button>
          }
        />
      ) : (
        <InvoiceForm
          clients={clients}
          defaultClientId={clients.some((c) => c.id === client) ? client : undefined}
          defaultCurrency={studio.default_currency}
        />
      )}
    </div>
  );
}
