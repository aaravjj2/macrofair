export default function MethodologyPage() {
  return (
    <section className="space-y-4" data-testid="methodology-page">
      <div className="panel rounded-2xl p-6">
        <p className="text-xs uppercase tracking-[0.2em] muted">Methodology</p>
        <h2 className="mt-2 text-2xl font-semibold">How MacroFair estimates fair value</h2>
        <p className="mt-3 max-w-3xl text-sm muted">
          MacroFair blends market microstructure with macro fundamentals in a deterministic baseline model,
          then ranks dislocations by absolute gap and confidence quality.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <article className="panel rounded-2xl p-5">
          <h3 className="text-lg font-semibold">Model flow</h3>
          <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm muted">
            <li>Normalize Polymarket and Kalshi snapshots into a canonical schema.</li>
            <li>Map each contract to a macro target and linked FRED series.</li>
            <li>Build deterministic feature rows (probability, spread, liquidity, horizon, macro signal).</li>
            <li>Estimate fair probability and confidence using a transparent baseline formula.</li>
            <li>Rank by dislocation actionability and expose explanation factors.</li>
          </ol>
        </article>

        <article className="panel rounded-2xl p-5">
          <h3 className="text-lg font-semibold">Limitations</h3>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm muted">
            <li>V1 only covers macro categories and deterministic fixture snapshots.</li>
            <li>Low-liquidity contracts may carry wider uncertainty than score alone suggests.</li>
            <li>Model output is calibration-first research guidance, not execution advice.</li>
          </ul>
        </article>
      </div>
    </section>
  );
}
