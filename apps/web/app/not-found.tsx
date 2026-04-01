import Link from "next/link";

export default function NotFoundPage() {
  return (
    <section className="panel rounded-2xl p-8">
      <p className="text-xs uppercase tracking-[0.2em] muted">Not found</p>
      <h2 className="mt-2 text-2xl font-semibold">Market not found in demo snapshot</h2>
      <Link
        href="/"
        className="mt-4 inline-block rounded-md border border-slate-400/40 px-3 py-2 text-sm hover:border-slate-200"
        data-testid="not-found-home-link"
      >
        Return to screener
      </Link>
    </section>
  );
}
