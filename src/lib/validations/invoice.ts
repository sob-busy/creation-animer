import { z } from "zod";

import { CURRENCIES, toMinor } from "@/lib/money";

export const INVOICE_STATUSES = ["draft", "sent", "paid", "void"] as const;
export type InvoiceStatus = (typeof INVOICE_STATUSES)[number] | "overdue";

/** Allowed manual transitions (payments via Stripe also set "paid" server-side). */
export const TRANSITIONS: Record<string, readonly InvoiceStatus[]> = {
  draft: ["sent", "void"],
  sent: ["paid", "void"],
  overdue: ["paid", "void"],
  paid: [],
  void: [],
};

const isoDate = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Date invalide.");

const itemSchema = z.object({
  description: z.string().trim().min(1, "Description requise.").max(500),
  quantity: z
    .string()
    .trim()
    .transform((v) => v.replace(",", "."))
    .refine((v) => /^\d{1,5}(\.\d{1,3})?$/.test(v) && Number(v) > 0, "Quantité invalide.")
    .transform(Number),
  unitPrice: z.string().trim().min(1, "Prix requis."),
});

export const invoiceSchema = z
  .object({
    clientId: z.string().uuid("Choisissez un client."),
    currency: z.enum(CURRENCIES, { errorMap: () => ({ message: "Devise non prise en charge." }) }),
    taxRate: z
      .string()
      .trim()
      .transform((v) => (v === "" ? "0" : v.replace(",", ".")))
      .refine((v) => /^\d{1,3}(\.\d{1,2})?$/.test(v) && Number(v) <= 100, "Taux entre 0 et 100 %.")
      .transform((v) => Math.round(Number(v) * 100)), // → basis points
    issuedAt: isoDate,
    dueAt: z.union([isoDate, z.literal("")]).transform((v) => v || null),
    notes: z
      .string()
      .trim()
      .max(5000)
      .transform((v) => v || null),
    items: z
      .string()
      .transform((raw, ctx) => {
        try {
          return JSON.parse(raw) as unknown;
        } catch {
          ctx.addIssue({ code: "custom", message: "Lignes invalides." });
          return z.NEVER;
        }
      })
      .pipe(z.array(itemSchema).min(1, "Ajoutez au moins une ligne.").max(100, "100 lignes maximum.")),
  })
  .refine((d) => !d.dueAt || d.dueAt >= d.issuedAt, { message: "L'échéance précède l'émission.", path: ["dueAt"] })
  .transform((d, ctx) => {
    const items = d.items.map((it, i) => {
      const unit = toMinor(it.unitPrice, d.currency);
      if (unit === null) {
        ctx.addIssue({ code: "custom", message: `Ligne ${i + 1} : prix invalide pour ${d.currency}.`, path: ["items"] });
      }
      return { description: it.description, quantity: it.quantity, unit_price_minor: unit ?? 0 };
    });
    return { ...d, items };
  });

export const statusSchema = z.enum(["sent", "paid", "void"]);
