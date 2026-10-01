"use client";

import { Button } from "@/components/ui/button";

export default function DashboardError({ reset }: { error: Error; reset: () => void }) {
  return (
    <div role="alert" className="mx-auto grid max-w-md place-items-center gap-4 py-24 text-center">
      <h2 className="font-display text-2xl font-semibold">Un imprévu dans l&apos;atelier</h2>
      <p className="text-sm text-muted-foreground">Le chargement a échoué. Réessayez dans un instant.</p>
      <Button onClick={reset}>Réessayer</Button>
    </div>
  );
}
