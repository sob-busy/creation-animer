import { FileText, LayoutDashboard, type LucideIcon, Shirt, Sparkles, Store, Users } from "lucide-react";

export type NavItem = { href: string; label: string; short: string; icon: LucideIcon; soon?: boolean };

export const NAV_ITEMS: NavItem[] = [
  { href: "/dashboard", label: "Vue d'ensemble", short: "Accueil", icon: LayoutDashboard },
  { href: "/dashboard/designs", label: "Modèles IA", short: "Modèles", icon: Sparkles, soon: true },
  { href: "/dashboard/try-on", label: "Essayage", short: "Essayage", icon: Shirt, soon: true },
  { href: "/dashboard/clients", label: "Clients", short: "Clients", icon: Users },
  { href: "/dashboard/invoices", label: "Factures", short: "Factures", icon: FileText, soon: true },
  { href: "/dashboard/marketplace", label: "Marketplace", short: "Boutique", icon: Store, soon: true },
];
