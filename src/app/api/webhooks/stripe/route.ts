import { NextResponse } from "next/server";
import type Stripe from "stripe";
import { z } from "zod";

import { serverEnv } from "@/lib/env/server";
import { stripe } from "@/lib/stripe";
import { createAdminClient } from "@/lib/supabase/admin";

// Signature verification needs the exact raw body and Node crypto.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const MAX_BODY_BYTES = 512 * 1024;

/** Metadata we attach server-side when creating a PaymentIntent for an invoice. */
const paymentMetadata = z.object({
  studio_id: z.string().uuid(),
  invoice_id: z.string().uuid().optional(),
});

const STATUS: Partial<Record<Stripe.Event.Type, "succeeded" | "failed">> = {
  "payment_intent.succeeded": "succeeded",
  "payment_intent.payment_failed": "failed",
};

export async function POST(request: Request) {
  const signature = request.headers.get("stripe-signature");
  if (!signature) return NextResponse.json({ error: "Missing signature" }, { status: 400 });

  const length = Number(request.headers.get("content-length") ?? 0);
  if (length > MAX_BODY_BYTES) return NextResponse.json({ error: "Payload too large" }, { status: 413 });

  const body = await request.text();

  let event: Stripe.Event;
  try {
    // Verifies the HMAC signature and rejects events older than 5 minutes (replay protection).
    event = stripe().webhooks.constructEvent(body, signature, serverEnv("STRIPE_WEBHOOK_SECRET"));
  } catch {
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  const supabase = createAdminClient();

  // Idempotency: Stripe retries deliveries; skip events already processed.
  try {
    const { data: seen, error: seenError } = await supabase
      .from("stripe_events")
      .select("id")
      .eq("id", event.id)
      .maybeSingle();
    if (seenError) throw seenError;
    if (seen) return NextResponse.json({ received: true, duplicate: true });

    const status = STATUS[event.type];
    if (status) {
      const intent = event.data.object as Stripe.PaymentIntent;
      const meta = paymentMetadata.safeParse(intent.metadata);
      if (!meta.success) {
        // Not created by StyliZ (or tampered with) — acknowledge without writing anything.
        console.warn("[stripe] payment_intent without valid StyliZ metadata", event.id);
      } else {
        const { error } = await supabase.from("payments").upsert(
          {
            studio_id: meta.data.studio_id,
            invoice_id: meta.data.invoice_id ?? null,
            provider: "stripe",
            provider_payment_id: intent.id,
            amount_minor: status === "succeeded" ? intent.amount_received : intent.amount,
            currency: intent.currency.toUpperCase(),
            status,
          },
          { onConflict: "provider,provider_payment_id" },
        );
        if (error) throw error;

        if (status === "succeeded" && meta.data.invoice_id) {
          const { error: invoiceError } = await supabase
            .from("invoices")
            .update({ status: "paid" })
            .eq("id", meta.data.invoice_id)
            .eq("studio_id", meta.data.studio_id);
          if (invoiceError) throw invoiceError;
        }
      }
    }

    // Recorded only after successful processing so a failure lets Stripe retry.
    const { error: recordError } = await supabase.from("stripe_events").insert({ id: event.id, type: event.type });
    // Processing already succeeded and is idempotent: log, but don't make Stripe retry.
    if (recordError) console.error("[stripe] could not record event", event.id, recordError.message);
    return NextResponse.json({ received: true });
  } catch (err) {
    console.error("[stripe] webhook processing failed", event.id, err);
    // 500 → Stripe retries with backoff. No internal details in the response.
    return NextResponse.json({ error: "Processing failed" }, { status: 500 });
  }
}
