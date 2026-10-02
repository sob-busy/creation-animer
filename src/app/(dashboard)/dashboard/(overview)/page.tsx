import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight, FileText, Shirt, Sparkles, Users } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { requireUser } from "@/lib/auth";
import { createClient } from "@/lib/supabase/server";

export const metadata: Metadata = { title: "Vue d'ensemble" };

async function count(table: "clients" | "designs" | "try_on_sessions" | "invoices") {
  const supabase = await createClient();
  // RLS restricts the count to the user's studios.
  const { count: n } = await supabase.from(table).select("*", { count: "exact", head: true });
  return n ?? 0;
}

export default async function DashboardPage() {
  const user = await requireUser();
  const firstName = ((user.user_metadata?.full_name as string | undefined) ?? "").split(" ")[0];
  const [clients, designs, tryOns, invoices] = await Promise.all([
    count("clients"),
    count("designs"),
    count("try_on_sessions"),
    count("invoices"),
  ]);

  const stats = [
    { label: "Modèles", value: designs, icon: Sparkles },
    { label: "Essayages", value: tryOns, icon: Shirt },
    { label: "Clients", value: clients, icon: Users, href: "/dashboard/clients" },
    { label: "Factures", value: invoices, icon: FileText, href: "/dashboard/invoices" },
  ];

  const steps = [
    {
      title: "Générez votre premier modèle",
      text: "Décrivez une pièce, l'IA propose des variantes.",
      done: designs > 0,
    },
    {
      title: "Ajoutez une cliente et ses mesures",
      text: "Centralisez fiches, mesures et historique.",
      done: clients > 0,
      href: "/dashboard/clients/new",
    },
    { title: "Lancez un essayage virtuel", text: "Montrez le rendu avant la première coupe.", done: tryOns > 0 },
    {
      title: "Émettez une facture",
      text: "En XOF, EUR, USD… paiement en ligne via Stripe.",
      done: invoices > 0,
      href: "/dashboard/invoices/new",
    },
  ];

  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <div className="space-y-1">
        <p className="text-sm text-muted-foreground">Bonjour{firstName ? `, ${firstName}` : ""} 👋</p>
        <h1 className="font-display text-3xl font-semibold sm:text-4xl">Votre studio</h1>
      </div>

      <section aria-label="Indicateurs" className="grid grid-cols-2 gap-3 lg:grid-cols-4 lg:gap-4">
        {stats.map(({ label, value, icon: Icon, href }) => {
          const card = (
            <Card className={`h-full gap-3 py-5 ${href ? "transition-colors group-hover:border-brand/40" : ""}`}>
              <CardHeader className="flex flex-row items-center justify-between px-5">
                <CardDescription className="font-medium">{label}</CardDescription>
                <span className="grid size-8 place-items-center rounded-md bg-accent text-accent-foreground">
                  <Icon className="size-4" aria-hidden />
                </span>
              </CardHeader>
              <CardContent className="px-5">
                <p className="font-display text-3xl font-semibold tabular-nums">{value}</p>
              </CardContent>
            </Card>
          );
          return href ? (
            <Link
              key={label}
              href={href}
              className="group rounded-xl outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50"
            >
              {card}
            </Link>
          ) : (
            <div key={label}>{card}</div>
          );
        })}
      </section>

      <Card>
        <CardHeader>
          <CardTitle className="font-display text-xl">Premiers pas</CardTitle>
          <CardDescription>Quatre étapes pour mettre votre atelier en ligne.</CardDescription>
        </CardHeader>
        <CardContent>
          <ol className="grid gap-3 sm:grid-cols-2">
            {steps.map((step, i) => (
              <li key={step.title}>
                <StepWrapper href={step.href}>
                  <span
                    className={
                      step.done
                        ? "grid size-8 shrink-0 place-items-center rounded-full bg-success text-xs font-semibold text-white"
                        : "grid size-8 shrink-0 place-items-center rounded-full border text-xs font-semibold text-muted-foreground"
                    }
                    aria-label={step.done ? "Terminé" : `Étape ${i + 1}`}
                  >
                    {step.done ? "✓" : i + 1}
                  </span>
                  <div className="min-w-0">
                    <p className="flex items-center gap-1 font-medium">
                      {step.title}
                      {step.href && (
                        <ArrowUpRight
                          className="size-3.5 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100"
                          aria-hidden
                        />
                      )}
                    </p>
                    <p className="mt-0.5 text-sm text-muted-foreground">{step.text}</p>
                  </div>
                </StepWrapper>
              </li>
            ))}
          </ol>
        </CardContent>
      </Card>
    </div>
  );
}

function StepWrapper({ href, children }: { href?: string; children: React.ReactNode }) {
  const cls = "group flex h-full gap-4 rounded-lg border bg-background p-4 transition-colors";
  if (!href) return <div className={cls}>{children}</div>;
  return (
    <Link
      href={href}
      className={`${cls} outline-none hover:border-brand/40 focus-visible:ring-[3px] focus-visible:ring-ring/50`}
    >
      {children}
    </Link>
  );
}
