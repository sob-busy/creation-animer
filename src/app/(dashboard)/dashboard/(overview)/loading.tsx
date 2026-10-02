export default function Loading() {
  return (
    <div className="mx-auto max-w-6xl animate-pulse space-y-8" aria-busy aria-label="Chargement">
      <div className="space-y-2">
        <div className="h-4 w-32 rounded bg-muted" />
        <div className="h-9 w-56 rounded bg-muted" />
      </div>
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4 lg:gap-4">
        {Array.from({ length: 4 }, (_, i) => (
          <div key={i} className="h-28 rounded-xl bg-muted" />
        ))}
      </div>
      <div className="h-72 rounded-xl bg-muted" />
    </div>
  );
}
