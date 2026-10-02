import type { Metadata } from "next";
import Link from "next/link";
import { ChevronRight, FileText, Plus } from "lucide-react";

import { StatusBadge } from "@/components/invoices/status-badge";
import { EmptyState } from "@/components/layout/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { formatMoney } from "@/lib/money";
import { getCurrentStudio } from "@/lib/studio";
import { createClient } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Factures" };

const fmtDate = (d: string | null) => (d ? new Date(d).toLocaleDateString("fr-FR", { dateStyle: "medium" }) : "—");

export default async function InvoicesPage() {
  await getCurrentStudio();
  const supabase = await createClient();
  const { data: invoices } = await supabase
    .from("invoices")
    .select("id, number, status, currency, total_minor, issued_at, due_at, clients(full_name)")
    .order("created_at", { ascending: false })
    .limit(100);

  // Outstanding amounts per currency (never summed across currencies).
  const outstanding = new Map<string, number>();
  for (const inv of invoices ?? []) {
    if (inv.status === "sent" || inv.status === "overdue") {
      outstanding.set(inv.currency, (outstanding.get(inv.currency) ?? 0) + inv.total_minor);
    }
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <PageHeader
        title="Factures"
        description={
          outstanding.size
            ? `À encaisser : ${[...outstanding].map(([c, v]) => formatMoney(v, c)).join(" · ")}`
            : "Facturation multi-devises de votre studio."
        }
        actions={
          <Button asChild>
            <Link href="/dashboard/invoices/new">
              <Plus aria-hidden /> Nouvelle facture
            </Link>
          </Button>
        }
      />

      {!invoices?.length ? (
        <EmptyState
          icon={FileText}
          title="Aucune facture"
          text="Créez une facture en XOF, EUR, USD… Les totaux et la TVA sont calculés automatiquement."
          action={
            <Button asChild>
              <Link href="/dashboard/invoices/new">
                <Plus aria-hidden /> Créer une facture
              </Link>
            </Button>
          }
        />
      ) : (
        <ul className="divide-y overflow-hidden rounded-xl border bg-card">
          {invoices.map((inv) => {
            const client = inv.clients as unknown as { full_name: string } | null;
            return (
              <li key={inv.id}>
                <Link
                  href={`/dashboard/invoices/${inv.id}`}
                  className="grid grid-cols-[1fr_auto] items-center gap-x-4 gap-y-1 px-4 py-3.5 transition-colors outline-none hover:bg-secondary/60 focus-visible:bg-secondary sm:grid-cols-[8rem_1fr_7rem_9rem_1rem] sm:px-5"
                >
                  <span className="font-mono text-sm">{inv.number}</span>
                  <span className="text-right font-semibold tabular-nums sm:order-4">{formatMoney(inv.total_minor, inv.currency)}</span>
                  <span className="truncate text-sm text-muted-foreground sm:order-2 sm:text-base sm:text-foreground">
                    {client?.full_name ?? "—"}
                    {inv.due_at && <span className="sm:hidden"> · échéance {fmtDate(inv.due_at)}</span>}
                  </span>
                  <span className="justify-self-end sm:order-3 sm:justify-self-start">
                    <StatusBadge status={inv.status} dueAt={inv.due_at} />
                  </span>
                  <ChevronRight className="hidden size-4 text-muted-foreground sm:order-5 sm:block" aria-hidden />
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
