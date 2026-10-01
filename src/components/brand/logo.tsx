import Link from "next/link";

import { cn } from "@/lib/utils";

export function Logo({ className, href = "/" }: { className?: string; href?: string }) {
  return (
    <Link
      href={href}
      className={cn("inline-flex items-center gap-2 rounded-md font-display text-xl font-semibold tracking-tight outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50", className)}
      aria-label="StyliZ — accueil"
    >
      <span aria-hidden className="grid size-8 place-items-center rounded-lg bg-primary text-primary-foreground">
        <span className="font-display text-lg italic leading-none">S</span>
      </span>
      <span>
        Styli<span className="text-brand">Z</span>
      </span>
    </Link>
  );
}
