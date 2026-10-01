import "server-only";

import Stripe from "stripe";

import { serverEnv } from "@/lib/env/server";

let client: Stripe | undefined;

/** Server-side Stripe client (secret key never leaves the server). */
export function stripe() {
  client ??= new Stripe(serverEnv("STRIPE_SECRET_KEY"), {
    appInfo: { name: "StyliZ" },
    maxNetworkRetries: 2,
  });
  return client;
}
