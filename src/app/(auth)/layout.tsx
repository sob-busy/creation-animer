import { Logo } from "@/components/brand/logo";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid min-h-dvh lg:grid-cols-[1.05fr_1fr]">
      {/* Brand panel — desktop only, keeps forms focused on mobile */}
      <aside className="relative hidden overflow-hidden bg-primary text-primary-foreground lg:flex lg:flex-col lg:justify-between lg:p-12">
        <div
          aria-hidden
          className="pointer-events-none absolute -top-32 -right-32 size-[28rem] rounded-full bg-brand/30 blur-3xl"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute bottom-0 left-0 h-64 w-full bg-[repeating-linear-gradient(135deg,transparent_0_22px,rgb(255_255_255/0.035)_22px_23px)]"
        />
        <Logo className="relative text-primary-foreground [&>span:first-child]:bg-primary-foreground [&>span:first-child]:text-primary" />
        <blockquote className="relative max-w-md space-y-4">
          <p className="font-display text-3xl leading-snug">
            « De l&apos;idée au vêtement porté — dessinez, essayez et facturez au même endroit. »
          </p>
          <footer className="text-sm text-primary-foreground/60">iziFashion Studio</footer>
        </blockquote>
      </aside>

      <main className="flex flex-col px-4 py-8 sm:px-8">
        <Logo className="mb-10 lg:hidden" />
        <div className="mx-auto flex w-full max-w-sm flex-1 flex-col justify-center">{children}</div>
      </main>
    </div>
  );
}
