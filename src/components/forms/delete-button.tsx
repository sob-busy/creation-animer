"use client";

import { useState, useTransition } from "react";
import { Loader2, Trash2 } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import type { FormState } from "@/lib/validations/form";

/** Two-step destructive button: first click arms it, second confirms. */
export function DeleteButton({ action, label = "Supprimer" }: { action: () => Promise<FormState>; label?: string }) {
  const [armed, setArmed] = useState(false);
  const [pending, startTransition] = useTransition();

  return (
    <div className="flex flex-wrap items-center gap-2">
      <Button
        type="button"
        variant={armed ? "destructive" : "outline"}
        disabled={pending}
        onClick={() => {
          if (!armed) return setArmed(true);
          startTransition(async () => {
            const res = await action();
            if (res?.error) {
              toast.error(res.error);
              setArmed(false);
            }
          });
        }}
      >
        {pending ? <Loader2 className="animate-spin" aria-hidden /> : <Trash2 aria-hidden />}
        {armed ? "Confirmer la suppression" : label}
      </Button>
      {armed && !pending && (
        <Button type="button" variant="ghost" onClick={() => setArmed(false)}>
          Annuler
        </Button>
      )}
    </div>
  );
}
