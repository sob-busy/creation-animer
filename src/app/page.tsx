import Link from "next/link";
import { ArrowRight, Banknote, Shirt, Sparkles, Store, Users } from "lucide-react";

import { Logo } from "@/components/brand/logo";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const FEATURES = [
  {
    icon: Sparkles,
    title: "Création assistée par IA",
    text: "Décrivez une coupe, un tissu, une ambiance : obtenez des variantes prêtes à affiner.",
  },
  {
    icon: Shirt,
    title: "Essayage virtuel",
    text: "Montrez à vos clientes le rendu porté avant la première coupe de tissu.",
  },
  {
    icon: Users,
    title: "Clients & mesures",
    text: "Fiches clientes, mesures et historique des commandes, au même endroit.",
  },
  {
    icon: Banknote,
    title: "Facturation multi-devises",
    text: "XOF, EUR, USD… factures claires et paiement en ligne sécurisé.",
  },
  {
    icon: Store,
    title: "Marketplace",
    text: "Publiez vos créations et vendez au-delà de votre quartier.",
  },
];

function HeroVisual() {
  // Pure-CSS composition (no image request): a "design card" and a "try-on" card.
  return (
    <div aria-hidden className="relative mx-auto aspect-[4/5] w-full max-w-sm select-none lg:max-w-md">
      <div className="absolute inset-0 rounded-[2rem] bg-gradient-to-br from-accent via-secondary to-background" />
      <div className="absolute top-8 left-6 right-16 rotate-[-4deg] rounded-2xl border bg-card p-4 shadow-xl transition-transform duration-500 hover:rotate-0">
        <div className="mb-3 flex items-center gap-2 text-xs font-medium text-muted-foreground">
          <Sparkles className="size-3.5 text-brand" /> Modèle généré
        </div>
        <div className="aspect-[3/4] rounded-xl bg-[radial-gradient(circle_at_30%_20%,var(--brand)_0,transparent_45%),repeating-linear-gradient(115deg,var(--secondary)_0_14px,var(--accent)_14px_28px)] opacity-90" />
        <p className="mt-3 font-display text-lg">Robe portefeuille wax</p>
        <p className="text-xs text-muted-foreground">Coton · coupe midi · col V</p>
      </div>
      <div className="absolute right-4 bottom-10 w-44 rotate-[5deg] rounded-2xl border bg-card p-3 shadow-lg transition-transform duration-500 hover:rotate-0">
        <div className="flex items-center gap-2 text-xs font-medium">
          <span className="size-2 rounded-full bg-success" /> Essayage prêt
        </div>
        <div className="mt-2 h-20 rounded-lg bg-gradient-to-t from-primary/80 to-brand/60" />
        <p className="mt-2 text-xs text-muted-foreground">Facture · 45 000 XOF</p>
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <div className="flex min-h-dvh flex-col">
      <header className="sticky top-0 z-30 border-b border-transparent bg-background/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
          <Logo />
          <nav className="flex items-center gap-1 sm:gap-2">
            <Button asChild variant="ghost" size="sm">
              <Link href="/login">Connexion</Link>
            </Button>
            <Button asChild size="sm">
              <Link href="/signup">Commencer</Link>
            </Button>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <section className="mx-auto grid max-w-6xl items-center gap-12 px-4 py-16 sm:px-6 lg:grid-cols-[1.1fr_1fr] lg:py-24">
          <div className="space-y-8">
            <p className="inline-flex items-center gap-2 rounded-full border bg-card px-3 py-1 text-xs font-medium text-muted-foreground">
              <span className="size-1.5 rounded-full bg-brand" /> iziFashion Studio
            </p>
            <h1 className="font-display text-4xl leading-[1.05] font-semibold text-balance sm:text-5xl lg:text-6xl">
              Votre atelier de mode, <em className="text-brand">augmenté</em> par l&apos;IA.
            </h1>
            <p className="max-w-xl text-lg text-pretty text-muted-foreground">
              Créez des modèles, faites-les essayer virtuellement, puis gérez clientes, factures et ventes — sans
              changer d&apos;outil.
            </p>
            <div className="flex flex-col gap-3 sm:flex-row">
              <Button asChild size="lg" className="group">
                <Link href="/signup">
                  Créer mon studio gratuitement
                  <ArrowRight className="transition-transform group-hover:translate-x-0.5" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/login">J&apos;ai déjà un compte</Link>
              </Button>
            </div>
          </div>
          <HeroVisual />
        </section>

        <section aria-labelledby="features" className="border-t bg-card/50">
          <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 lg:py-24">
            <h2 id="features" className="max-w-2xl font-display text-3xl font-semibold sm:text-4xl">
              Tout le cycle d&apos;une création, de l&apos;idée au paiement.
            </h2>
            <ul className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {FEATURES.map(({ icon: Icon, title, text }, i) => (
                <li
                  key={title}
                  className={cn(
                    "group rounded-xl border bg-background p-6 transition-all duration-200 hover:-translate-y-0.5 hover:border-brand/40 hover:shadow-md",
                    // Feature the core AI capability; also fills the 3-column grid (2 + 1 / 3).
                    i === 0 && "bg-gradient-to-br from-accent/70 via-background to-background lg:col-span-2",
                  )}
                >
                  <span className="grid size-10 place-items-center rounded-lg bg-accent text-accent-foreground transition-colors group-hover:bg-brand group-hover:text-brand-foreground">
                    <Icon className="size-5" aria-hidden />
                  </span>
                  <h3 className={cn("mt-4 font-semibold", i === 0 && "font-display text-xl")}>{title}</h3>
                  <p className="mt-1.5 max-w-md text-sm text-muted-foreground">{text}</p>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </main>

      <footer className="border-t">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-2 px-4 py-6 text-sm text-muted-foreground sm:flex-row sm:px-6">
          <p>© {new Date().getFullYear()} StyliZ — iziFashion Studio</p>
          <p>Conçu pour les créateurs et ateliers de mode.</p>
        </div>
      </footer>
    </div>
  );
}
