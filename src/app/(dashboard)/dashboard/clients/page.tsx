import type { Metadata } from "next";
import Link from "next/link";
import { ChevronRight, Plus, Search, Users } from "lucide-react";

import { EmptyState } from "@/components/layout/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getCurrentStudio } from "@/lib/studio";
import { createClient } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Clients" };

/** Keep only characters that cannot alter PostgREST filter syntax. */
function sanitizeSearch(q: unknown) {
  return typeof q === "string" ? q.replace(/[^\p{L}\p{N} @.+'-]/gu, "").trim().slice(0, 60) : "";
}

export default async function ClientsPage({ searchParams }: { searchParams: Promise<{ q?: string }> }) {
  await getCurrentStudio();
  const q = sanitizeSearch((await searchParams).q);

  const supabase = await createClient();
  let query = supabase
    .from("clients")
    .select("id, full_name, email, phone, updated_at")
    .order("full_name")
    .limit(100);
  if (q) query = query.or(`full_name.ilike.%${q}%,email.ilike.%${q}%,phone.ilike.%${q}%`);
  const { data: clients = [] } = await query;

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <PageHeader
        title="Clients"
        description="Fiches, coordonnées et mesures de votre clientèle."
        actions={
          <Button asChild>
            <Link href="/dashboard/clients/new">
              <Plus aria-hidden /> Nouveau client
            </Link>
          </Button>
        }
      />

      <form role="search" className="relative max-w-sm">
        <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden />
        <Input name="q" type="search" defaultValue={q} placeholder="Rechercher nom, e-mail, téléphone…" aria-label="Rechercher un client" className="pl-9" />
      </form>

      {!clients?.length ? (
        <EmptyState
          icon={Users}
          title={q ? "Aucun résultat" : "Aucun client pour l'instant"}
          text={q ? `Aucun client ne correspond à « ${q} ».` : "Ajoutez votre première cliente pour centraliser coordonnées et mesures."}
          action={
            !q && (
              <Button asChild>
                <Link href="/dashboard/clients/new">
                  <Plus aria-hidden /> Ajouter un client
                </Link>
              </Button>
            )
          }
        />
      ) : (
        <ul className="divide-y overflow-hidden rounded-xl border bg-card">
          {clients.map((c) => (
            <li key={c.id}>
              <Link
                href={`/dashboard/clients/${c.id}`}
                className="flex items-center gap-4 px-4 py-3.5 transition-colors outline-none hover:bg-secondary/60 focus-visible:bg-secondary sm:px-5"
              >
                <span aria-hidden className="grid size-9 shrink-0 place-items-center rounded-full bg-accent text-xs font-semibold text-accent-foreground">
                  {c.full_name.slice(0, 1).toUpperCase()}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block truncate font-medium">{c.full_name}</span>
                  <span className="block truncate text-sm text-muted-foreground">
                    {[c.phone, c.email].filter(Boolean).join(" · ") || "Aucune coordonnée"}
                  </span>
                </span>
                <ChevronRight className="size-4 shrink-0 text-muted-foreground" aria-hidden />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
