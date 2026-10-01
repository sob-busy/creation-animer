import { Logo } from "@/components/brand/logo";
import { MobileTabBar, SidebarNav } from "@/components/dashboard/sidebar-nav";
import { UserMenu } from "@/components/dashboard/user-menu";
import { requireUser } from "@/lib/auth";

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const user = await requireUser();
  const name = (user.user_metadata?.full_name as string | undefined) ?? user.email ?? "Mon compte";

  return (
    <div className="min-h-dvh md:grid md:grid-cols-[16rem_1fr]">
      <aside className="sticky top-0 hidden h-dvh flex-col border-r border-sidebar-border bg-sidebar px-3 py-5 md:flex">
        <Logo href="/dashboard" className="mb-8 px-3" />
        <SidebarNav />
        <div className="mt-auto rounded-lg border border-dashed bg-background/60 p-4 text-xs text-muted-foreground">
          <p className="font-medium text-foreground">Plan Découverte</p>
          <p className="mt-1">Les modules IA arrivent bientôt dans votre studio.</p>
        </div>
      </aside>

      <div className="flex min-w-0 flex-col">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b bg-background/80 px-4 backdrop-blur-md sm:px-6 lg:px-8">
          <Logo href="/dashboard" className="md:hidden" />
          <span className="hidden text-sm text-muted-foreground md:block">iziFashion Studio</span>
          <UserMenu name={name} email={user.email ?? ""} />
        </header>
        <main className="flex-1 px-4 pt-6 pb-24 sm:px-6 md:pb-10 lg:px-8">{children}</main>
      </div>

      <MobileTabBar />
    </div>
  );
}
