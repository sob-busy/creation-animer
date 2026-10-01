import Link from "next/link";

import { Logo } from "@/components/brand/logo";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <main className="grid min-h-dvh place-items-center px-4">
      <div className="grid max-w-md justify-items-center gap-5 text-center">
        <Logo />
        <p className="font-display text-7xl font-semibold text-brand">404</p>
        <h1 className="font-display text-2xl font-semibold">Cette page n&apos;est pas dans la collection</h1>
        <p className="text-sm text-muted-foreground">Le lien est peut-être erroné ou la page a été déplacée.</p>
        <Button asChild>
          <Link href="/">Retour à l&apos;accueil</Link>
        </Button>
      </div>
    </main>
  );
}
