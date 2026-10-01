"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

import { NAV_ITEMS } from "./nav-items";

/** Vertical navigation (desktop). */
export function SidebarNav() {
  const pathname = usePathname();
  return (
    <nav aria-label="Navigation principale" className="grid gap-1">
      {NAV_ITEMS.map(({ href, label, icon: Icon, soon }) => {
        const active = pathname === href;
        if (soon) {
          return (
            <span
              key={href}
              aria-disabled
              className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground/60"
            >
              <Icon className="size-4" aria-hidden />
              {label}
              <span className="ml-auto rounded-full bg-secondary px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-muted-foreground">
                Bientôt
              </span>
            </span>
          );
        }
        return (
          <Link
            key={href}
            href={href}
            aria-current={active ? "page" : undefined}
            className={cn(
              "relative flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50",
              active
                ? "bg-sidebar-accent text-foreground before:absolute before:inset-y-2 before:-left-3 before:w-0.5 before:rounded-full before:bg-brand"
                : "text-sidebar-foreground/80 hover:bg-sidebar-accent/60 hover:text-foreground",
            )}
          >
            <Icon className="size-4" aria-hidden />
            {label}
          </Link>
        );
      })}
    </nav>
  );
}

/** Bottom tab bar (mobile) — thumb-reachable, shows the 5 main sections. */
export function MobileTabBar() {
  const pathname = usePathname();
  return (
    <nav
      aria-label="Navigation principale"
      className="fixed inset-x-0 bottom-0 z-40 grid grid-cols-5 border-t bg-background/90 pb-[env(safe-area-inset-bottom)] backdrop-blur-md md:hidden"
    >
      {NAV_ITEMS.slice(0, 5).map(({ href, short, icon: Icon, soon }) => {
        const active = pathname === href;
        const content = (
          <>
            <Icon className={cn("size-5", active && "text-brand")} aria-hidden />
            <span className="max-w-full truncate">{short}</span>
          </>
        );
        const cls = cn(
          "flex h-16 flex-col items-center justify-center gap-1 px-1 text-[11px] font-medium",
          active ? "text-foreground" : "text-muted-foreground",
          soon && "opacity-50",
        );
        return soon ? (
          <span key={href} aria-disabled className={cls}>
            {content}
          </span>
        ) : (
          <Link key={href} href={href} aria-current={active ? "page" : undefined} className={cls}>
            {content}
          </Link>
        );
      })}
    </nav>
  );
}
