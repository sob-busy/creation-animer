import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { CreatedToast } from "@/components/forms/created-toast";
import { DeleteButton } from "@/components/forms/delete-button";
import { StatusActions } from "@/components/invoices/status-actions";
import { effectiveStatus, StatusBadge } from "@/components/invoices/status-badge";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent } from "@/components/ui/card";
import { formatMoney } from "@/lib/money";
import { canManage, getCurrentStudio } from "@/lib/studio";
import { createClient } from "@/lib/supabase/server";
import { uuidSchema } from "@/lib/validations/client";
import { TRANSITIONS } from "@/lib/validations/invoice";

import { deleteInvoiceAction, setInvoiceStatusAction } from "../actions";

export const metadata: Metadata = { title: "Facture" };

const fmtDate = (d: string | null) => (d ? new Date(d).toLocaleDateString("fr-FR", { dateStyle: "long" }) : "—");

export default async function InvoicePage({
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
  const { data: inv } = await supabase
    .from("invoices")
    .select(
      "id, number, status, currency, issued_at, due_at, notes, subtotal_minor, tax_minor, total_minor, tax_rate_bp, clients(full_name, email, phone), invoice_items(id, description, quantity, unit_price_minor, position)",
    )
    .eq("id", id)
    .maybeSingle();
  if (!inv) notFound();

  const client = inv.clients as unknown as { full_name: string; email: string | null; phone: string | null };
  const items = [...(inv.invoice_items as { id: string; description: string; quantity: number; unit_price_minor: number; position: number }[])].sort(
    (a, b) => a.position - b.position,
  );
  const status = effectiveStatus(inv.status, inv.due_at);

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      {(await searchParams).created && <CreatedToast message="Brouillon de facture créé." />}
      <div className="print:hidden">
        <PageHeader
          title={`Facture ${inv.number}`}
          description={<StatusBadge status={inv.status} dueAt={inv.due_at} />}
          back={{ href: "/dashboard/invoices", label: "Factures" }}
        />
      </div>

      <StatusActions allowed={TRANSITIONS[status] ?? []} action={setInvoiceStatusAction.bind(null, inv.id)} />

      {/* Printable document */}
      <Card className="gap-0 py-0 print:border-0 print:shadow-none">
        <CardContent className="space-y-10 p-6 sm:p-10">
          <div className="flex flex-col justify-between gap-6 sm:flex-row">
            <div>
              <p className="font-display text-2xl font-semibold">{studio.name}</p>
              <p className="text-sm text-muted-foreground">via StyliZ</p>
            </div>
            <div className="text-sm sm:text-right">
              <p className="font-display text-xl font-semibold">Facture</p>
              <p className="font-mono">{inv.number}</p>
              <p className="mt-2 text-muted-foreground">Émise le {fmtDate(inv.issued_at)}</p>
              {inv.due_at && <p className="text-muted-foreground">Échéance : {fmtDate(inv.due_at)}</p>}
            </div>
          </div>

          <div className="text-sm">
            <p className="text-xs font-medium tracking-wide text-muted-foreground uppercase">Facturé à</p>
            <p className="mt-1 font-medium">{client.full_name}</p>
            {client.email && <p className="text-muted-foreground">{client.email}</p>}
            {client.phone && <p className="text-muted-foreground">{client.phone}</p>}
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-xs text-muted-foreground">
                  <th className="pb-2 font-medium">Description</th>
                  <th className="pb-2 text-right font-medium">Qté</th>
                  <th className="pb-2 text-right font-medium">Prix unitaire</th>
                  <th className="pb-2 text-right font-medium">Total</th>
                </tr>
              </thead>
              <tbody className="tabular-nums">
                {items.map((it) => (
                  <tr key={it.id} className="border-b last:border-0">
                    <td className="py-3 pr-4">{it.description}</td>
                    <td className="py-3 text-right">{Number(it.quantity).toLocaleString("fr-FR")}</td>
                    <td className="py-3 text-right whitespace-nowrap">{formatMoney(it.unit_price_minor, inv.currency)}</td>
                    <td className="py-3 text-right whitespace-nowrap">
                      {formatMoney(Math.round(Number(it.quantity) * it.unit_price_minor), inv.currency)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <dl className="ml-auto grid w-full max-w-xs gap-2 text-sm tabular-nums">
            <div className="flex justify-between text-muted-foreground">
              <dt>Sous-total</dt>
              <dd>{formatMoney(inv.subtotal_minor, inv.currency)}</dd>
            </div>
            <div className="flex justify-between text-muted-foreground">
              <dt>TVA ({(inv.tax_rate_bp / 100).toLocaleString("fr-FR")} %)</dt>
              <dd>{formatMoney(inv.tax_minor, inv.currency)}</dd>
            </div>
            <div className="flex justify-between border-t pt-2 text-base font-semibold">
              <dt>Total</dt>
              <dd>{formatMoney(inv.total_minor, inv.currency)}</dd>
            </div>
          </dl>

          {inv.notes && <p className="border-t pt-6 text-sm whitespace-pre-line text-muted-foreground">{inv.notes}</p>}
        </CardContent>
      </Card>

      {inv.status === "draft" && canManage(studio) && (
        <div className="print:hidden">
          <DeleteButton action={deleteInvoiceAction.bind(null, inv.id)} label="Supprimer le brouillon" />
        </div>
      )}
    </div>
  );
}
