import Link from "next/link";

import {
  FLAGSHIP_PERSISTENCE_SNAPSHOTS,
  FLAGSHIP_SNAPSHOT_HEADLINE,
  SECONDARY_FINDING_ONE_SENTENCE,
  SECONDARY_FINDING_SNAPSHOTS,
  THIRD_FINDING_CATEGORY_DRIFT,
  THIRD_FINDING_ONE_SENTENCE,
} from "@/lib/findings-data";
import {
  summarizeFlagshipPersistence,
  summarizeSecondaryFinding,
  summarizeThirdFinding,
} from "@/lib/findings-utils";

function formatPct(value: number): string {
  return `${(value * 100).toFixed(2)}%`;
}

export default function MethodologyPage() {
  const persistence = summarizeFlagshipPersistence(FLAGSHIP_PERSISTENCE_SNAPSHOTS);
  const secondary = summarizeSecondaryFinding(SECONDARY_FINDING_SNAPSHOTS);
  const third = summarizeThirdFinding(THIRD_FINDING_CATEGORY_DRIFT);

  return (
    <section className="space-y-4" data-testid="methodology-page">
      <div className="panel rounded-2xl p-6">
        <p className="text-xs uppercase tracking-[0.2em] muted">Methodology</p>
        <h2 className="mt-2 text-2xl font-semibold">How MacroFair estimates fair value</h2>
        <p className="mt-3 max-w-3xl text-sm muted">
          MacroFair blends market microstructure with macro fundamentals in a deterministic combined model,
          then ranks contracts by how strongly crowd price diverges from fair value.
        </p>
      </div>

      <article className="panel rounded-2xl p-5" data-testid="methodology-findings-evidence">
        <h3 className="text-lg font-semibold">Findings evidence layer</h3>
        <p className="mt-2 text-sm muted">{FLAGSHIP_SNAPSHOT_HEADLINE}</p>
        <p className="mt-2 text-sm muted">
          Persistence check: {persistence.dominantTopMarketTitle} remains top in {formatPct(persistence.persistenceRate)} of
          deterministic snapshots.
        </p>
        <p className="text-sm muted">
          Secondary check: {SECONDARY_FINDING_ONE_SENTENCE} (average asymmetry {(secondary.averageAsymmetryGap * 100).toFixed(2)} pts).
        </p>
        <p className="text-sm muted">
          Third check: {THIRD_FINDING_ONE_SENTENCE} (dominant drift {(third.dominantDrift * 100).toFixed(2)} pts).
        </p>
        <Link
          href="/findings"
          className="mt-3 inline-block rounded-md border border-slate-300/40 px-3 py-2 text-sm hover:border-slate-100"
          data-testid="methodology-findings-link"
        >
          Open full findings evidence
        </Link>
      </article>

      <div className="grid gap-4 md:grid-cols-2" data-testid="methodology-sections">
        <article className="panel rounded-2xl p-5">
          <h3 className="text-lg font-semibold">Fair value</h3>
          <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm muted">
            <li>Normalize Polymarket and Kalshi snapshots into a canonical schema.</li>
            <li>Map each contract to a macro target and linked FRED series.</li>
            <li>Build deterministic feature rows (probability, spread, liquidity, horizon, macro signal).</li>
            <li>Estimate fair probability using baseline + fundamentals blend and deterministic calibration.</li>
          </ol>
        </article>

        <article className="panel rounded-2xl p-5">
          <h3 className="text-lg font-semibold">Confidence</h3>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm muted">
            <li>Higher liquidity and tighter spreads increase confidence.</li>
            <li>Stable market-to-macro mapping increases confidence.</li>
            <li>Model disagreement lowers confidence.</li>
          </ul>
        </article>

        <article className="panel rounded-2xl p-5">
          <h3 className="text-lg font-semibold">Deterministic demo mode</h3>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm muted">
            <li>Demo mode is the default and requires no secrets.</li>
            <li>Fixtures in data/fixtures power all test and demo behavior.</li>
            <li>Repeated runs produce identical outputs and proof artifacts.</li>
          </ul>
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

      <article className="panel rounded-2xl p-5" data-testid="methodology-interpretation-section">
        <h3 className="text-lg font-semibold">How to interpret a dislocation</h3>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm muted">
          <li>Positive gap: market probability is above fair value.</li>
          <li>Negative gap: market probability is below fair value.</li>
          <li>Large absolute gap with high confidence is the primary triage signal.</li>
          <li>Always read explanation factors and warning flags before drawing conclusions.</li>
        </ul>
      </article>
    </section>
  );
}
