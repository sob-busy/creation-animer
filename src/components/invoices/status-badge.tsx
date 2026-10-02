import { Badge } from "@/components/ui/badge";

const CONFIG = {
  draft: { label: "Brouillon", variant: "outline" },
  sent: { label: "Envoyée", variant: "brand" },
  overdue: { label: "En retard", variant: "warning" },
  paid: { label: "Payée", variant: "success" },
  void: { label: "Annulée", variant: "default" },
} as const;

/** "sent" past its due date is displayed as overdue without a background job. */
export function effectiveStatus(status: string, dueAt: string | null): keyof typeof CONFIG {
  const today = new Date().toISOString().slice(0, 10);
  if ((status === "sent" || status === "overdue") && dueAt && dueAt < today) return "overdue";
  return (status in CONFIG ? status : "draft") as keyof typeof CONFIG;
}

export function StatusBadge({ status, dueAt }: { status: string; dueAt: string | null }) {
  const { label, variant } = CONFIG[effectiveStatus(status, dueAt)];
  return <Badge variant={variant}>{label}</Badge>;
}
