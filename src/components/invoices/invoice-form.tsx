"use client";

import { useActionState, useMemo, useState } from "react";
import { Plus, X } from "lucide-react";

import { FormAlert } from "@/components/forms/form-alert";
import { FormField } from "@/components/forms/form-field";
import { SubmitButton } from "@/components/forms/submit-button";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { NativeSelect } from "@/components/ui/native-select";
import { Textarea } from "@/components/ui/textarea";
import { CURRENCIES, formatMoney, toMinor } from "@/lib/money";
import type { FormState } from "@/lib/validations/form";

import { createInvoiceAction } from "@/app/(dashboard)/dashboard/invoices/actions";

type Line = { key: number; description: string; quantity: string; unitPrice: string };

let nextKey = 1;
const emptyLine = (): Line => ({ key: nextKey++, description: "", quantity: "1", unitPrice: "" });

function parseLines(raw?: string): Line[] {
  try {
    const arr = JSON.parse(raw ?? "") as Omit<Line, "key">[];
    if (Array.isArray(arr) && arr.length) return arr.map((l) => ({ ...l, key: nextKey++ }));
  } catch {}
  return [emptyLine()];
}

export function InvoiceForm({
  clients,
  defaultClientId,
  defaultCurrency,
}: {
  clients: { id: string; full_name: string }[];
  defaultClientId?: string;
  defaultCurrency: string;
}) {
  const [state, action] = useActionState<FormState, FormData>(createInvoiceAction, {});
  const v = state.values ?? {};
  const [currency, setCurrency] = useState(v.currency ?? defaultCurrency);
  const [taxRate, setTaxRate] = useState(v.taxRate ?? "0");
  const [lines, setLines] = useState<Line[]>(() => parseLines(v.items));
  const today = new Date().toISOString().slice(0, 10);

  const update = (key: number, patch: Partial<Line>) =>
    setLines((ls) => ls.map((l) => (l.key === key ? { ...l, ...patch } : l)));

  // Live preview only — the database recomputes the real totals.
  const preview = useMemo(() => {
    const subtotal = lines.reduce((sum, l) => {
      const unit = toMinor(l.unitPrice || "0", currency) ?? 0;
      const qty = Number(l.quantity.replace(",", ".")) || 0;
      return sum + Math.round(qty * unit);
    }, 0);
    const rate = Number(taxRate.replace(",", ".")) || 0;
    const tax = Math.round((subtotal * rate) / 100);
    return { subtotal, tax, total: subtotal + tax };
  }, [lines, currency, taxRate]);

  const itemsJson = JSON.stringify(lines.map(({ description, quantity, unitPrice }) => ({ description, quantity, unitPrice })));
  const err = (n: string) => state.fieldErrors?.[n];

  return (
    <form action={action} className="grid gap-6" noValidate>
      <FormAlert type="error" message={state.error} />
      <input type="hidden" name="items" value={itemsJson} />

      <Card>
        <CardHeader>
          <CardTitle>Informations</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-5 sm:grid-cols-2">
          <div className="grid gap-2 sm:col-span-2">
            <Label htmlFor="clientId">Client</Label>
            <NativeSelect id="clientId" name="clientId" defaultValue={v.clientId ?? defaultClientId ?? ""} aria-invalid={Boolean(err("clientId")) || undefined}>
              <option value="" disabled>
                Choisir un client…
              </option>
              {clients.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.full_name}
                </option>
              ))}
            </NativeSelect>
            {err("clientId") && <p className="text-xs font-medium text-destructive">{err("clientId")![0]}</p>}
          </div>
          <div className="grid gap-2">
            <Label htmlFor="currency">Devise</Label>
            <NativeSelect id="currency" name="currency" value={currency} onChange={(e) => setCurrency(e.target.value)}>
              {CURRENCIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </NativeSelect>
          </div>
          <FormField
            name="taxRate"
            label="TVA (%)"
            inputMode="decimal"
            value={taxRate}
            onChange={(e) => setTaxRate(e.target.value)}
            hint="18 % au Sénégal et en Côte d'Ivoire ; 0 si non assujetti."
            errors={err("taxRate")}
          />
          <FormField name="issuedAt" type="date" label="Date d'émission" defaultValue={v.issuedAt ?? today} errors={err("issuedAt")} />
          <FormField name="dueAt" type="date" label="Échéance" defaultValue={v.dueAt ?? ""} errors={err("dueAt")} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Prestations</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3">
          <div className="hidden grid-cols-[1fr_6rem_9rem_2.5rem] gap-3 px-1 text-xs font-medium text-muted-foreground sm:grid">
            <span>Description</span>
            <span>Qté</span>
            <span>Prix unitaire ({currency})</span>
          </div>
          {lines.map((line, i) => (
            <fieldset
              key={line.key}
              className="grid grid-cols-2 gap-3 rounded-lg border p-3 animate-in fade-in-0 slide-in-from-top-1 sm:grid-cols-[1fr_6rem_9rem_2.5rem] sm:border-0 sm:p-0"
            >
              <legend className="sr-only">Ligne {i + 1}</legend>
              <Input
                aria-label={`Description ligne ${i + 1}`}
                placeholder="Robe sur mesure, retouche…"
                value={line.description}
                onChange={(e) => update(line.key, { description: e.target.value })}
                className="col-span-2 sm:col-span-1"
              />
              <Input
                aria-label={`Quantité ligne ${i + 1}`}
                inputMode="decimal"
                value={line.quantity}
                onChange={(e) => update(line.key, { quantity: e.target.value })}
              />
              <Input
                aria-label={`Prix unitaire ligne ${i + 1}`}
                inputMode="decimal"
                placeholder="0"
                value={line.unitPrice}
                onChange={(e) => update(line.key, { unitPrice: e.target.value })}
              />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                aria-label={`Supprimer la ligne ${i + 1}`}
                disabled={lines.length === 1}
                onClick={() => setLines((ls) => ls.filter((l) => l.key !== line.key))}
                className="col-span-2 justify-self-end sm:col-span-1"
              >
                <X aria-hidden />
              </Button>
            </fieldset>
          ))}
          {err("items") && <p className="text-xs font-medium text-destructive">{err("items")![0]}</p>}
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="justify-self-start"
            disabled={lines.length >= 100}
            onClick={() => setLines((ls) => [...ls, emptyLine()])}
          >
            <Plus aria-hidden /> Ajouter une ligne
          </Button>

          <dl className="mt-4 ml-auto grid w-full max-w-xs gap-2 border-t pt-4 text-sm tabular-nums" aria-live="polite">
            <div className="flex justify-between text-muted-foreground">
              <dt>Sous-total</dt>
              <dd>{formatMoney(preview.subtotal, currency)}</dd>
            </div>
            <div className="flex justify-between text-muted-foreground">
              <dt>TVA</dt>
              <dd>{formatMoney(preview.tax, currency)}</dd>
            </div>
            <div className="flex justify-between text-base font-semibold">
              <dt>Total</dt>
              <dd>{formatMoney(preview.total, currency)}</dd>
            </div>
          </dl>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>
            <Label htmlFor="notes">Notes</Label>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Textarea id="notes" name="notes" rows={3} placeholder="Conditions de paiement, acompte versé…" defaultValue={v.notes} />
        </CardContent>
      </Card>

      <div className="sm:ml-auto sm:w-56">
        <SubmitButton pendingLabel="Création…">Créer le brouillon</SubmitButton>
      </div>
    </form>
  );
}
