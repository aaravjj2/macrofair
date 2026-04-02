import Link from "next/link";

export function TopNav() {
  return (
    <header className="panel mb-6 rounded-2xl px-5 py-4">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-300">MacroFair</p>
          <h1 className="text-xl font-semibold">Crowd Odds vs Fundamentals</h1>
        </div>
        <nav className="flex items-center gap-3 text-sm">
          <Link
            href="/"
            className="rounded-md border border-slate-500/40 px-3 py-2 hover:border-slate-300"
            data-testid="nav-home-link"
          >
            Screener
          </Link>
          <Link
            href="/methodology"
            className="rounded-md border border-slate-500/40 px-3 py-2 hover:border-slate-300"
            data-testid="nav-methodology-link"
          >
            Methodology
          </Link>
          <Link
            href="/findings"
            className="rounded-md border border-slate-500/40 px-3 py-2 hover:border-slate-300"
            data-testid="nav-findings-link"
          >
            Findings
          </Link>
        </nav>
      </div>
    </header>
  );
}
