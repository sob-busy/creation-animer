import "server-only";

import { z } from "zod";

/**
 * Secret environment variables. The `server-only` import makes the build fail
 * if this module is ever imported from a Client Component.
 * Validated lazily so a missing optional integration (e.g. Stripe) does not
 * break unrelated pages.
 */
const schema = z.object({
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(20),
  STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_"),
});

type ServerEnv = z.infer<typeof schema>;

export function serverEnv<K extends keyof ServerEnv>(key: K): ServerEnv[K] {
  const parsed = schema.shape[key].safeParse(process.env[key]);
  if (!parsed.success) {
    throw new Error(`Variable d'environnement serveur ${key} invalide ou manquante. Voir .env.example.`);
  }
  return parsed.data as ServerEnv[K];
}
