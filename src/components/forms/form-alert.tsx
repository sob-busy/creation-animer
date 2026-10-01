import { CircleAlert, CircleCheck } from "lucide-react";

import { cn } from "@/lib/utils";

export function FormAlert({ type, message }: { type: "error" | "success"; message?: string }) {
  if (!message) return null;
  const Icon = type === "error" ? CircleAlert : CircleCheck;
  return (
    <div
      role={type === "error" ? "alert" : "status"}
      className={cn(
        "flex items-start gap-2 rounded-lg border px-3 py-2.5 text-sm animate-in fade-in-0 slide-in-from-top-1",
        type === "error"
          ? "border-destructive/30 bg-destructive/5 text-destructive"
          : "border-success/30 bg-success/5 text-success",
      )}
    >
      <Icon className="mt-0.5 size-4 shrink-0" aria-hidden />
      <span>{message}</span>
    </div>
  );
}
