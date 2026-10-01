export function AuthHeader({ title, description }: { title: string; description: string }) {
  return (
    <div className="mb-8 space-y-2">
      <h1 className="font-display text-3xl font-semibold">{title}</h1>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}
