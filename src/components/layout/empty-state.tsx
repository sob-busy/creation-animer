import type { LucideIcon } from "lucide-react";

export function EmptyState({
  icon: Icon,
  title,
  text,
  action,
}: {
  icon: LucideIcon;
  title: string;
  text: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="grid justify-items-center gap-3 rounded-xl border border-dashed bg-card/60 px-6 py-14 text-center">
      <span className="grid size-12 place-items-center rounded-full bg-accent text-accent-foreground">
        <Icon className="size-5" aria-hidden />
      </span>
      <h2 className="font-display text-xl font-semibold">{title}</h2>
      <p className="max-w-sm text-sm text-muted-foreground">{text}</p>
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}
