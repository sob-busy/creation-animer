"use client";

import { useTransition } from "react";
import { Ban, CheckCircle2, Loader2, Printer, Send } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import type { FormState } from "@/lib/validations/form";

const ACTIONS = {
  sent: { label: "Marquer envoyée", icon: Send, variant: "default" },
  paid: { label: "Marquer payée", icon: CheckCircle2, variant: "brand" },
  void: { label: "Annuler", icon: Ban, variant: "outline" },
} as const;

export function StatusActions({
  allowed,
  action,
}: {
  allowed: readonly string[];
  action: (next: string) => Promise<FormState>;
}) {
  const [pending, startTransition] = useTransition();

  return (
    <div className="flex flex-wrap gap-2 print:hidden">
      {allowed
        .filter((s): s is keyof typeof ACTIONS => s in ACTIONS)
        .map((s) => {
          const { label, icon: Icon, variant } = ACTIONS[s];
          return (
            <Button
              key={s}
              variant={variant}
              disabled={pending}
              onClick={() =>
                startTransition(async () => {
                  const res = await action(s);
                  if (res.error) toast.error(res.error);
                  else if (res.success) toast.success(res.success);
                })
              }
            >
              {pending ? <Loader2 className="animate-spin" aria-hidden /> : <Icon aria-hidden />}
              {label}
            </Button>
          );
        })}
      <Button variant="ghost" onClick={() => window.print()}>
        <Printer aria-hidden /> Imprimer / PDF
      </Button>
    </div>
  );
}
