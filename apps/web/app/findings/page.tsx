import {
  FLAGSHIP_PERSISTENCE_SNAPSHOTS,
  FLAGSHIP_SNAPSHOT_HEADLINE,
  LONGITUDINAL_WINDOW_NAME,
  SECONDARY_FINDING_ONE_SENTENCE,
  SECONDARY_FINDING_SNAPSHOTS,
} from "@/lib/findings-data";
import {
  summarizeFlagshipPersistence,
  summarizeSecondaryFinding,
} from "@/lib/findings-utils";

function formatPct(value: number): string {
  return `${(value * 100).toFixed(2)}%`;
}

function formatPts(value: number): string {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${(value * 100).toFixed(2)} pts`;
}

export default function FindingsPage() {
  const persistence = summarizeFlagshipPersistence(FLAGSHIP_PERSISTENCE_SNAPSHOTS);
  const secondary = summarizeSecondaryFinding(SECONDARY_FINDING_SNAPSHOTS);

  return (
    <section className="space-y-4" data-testid="findings-page">
      <div className="panel rounded-2xl p-6" data-testid="findings-snapshot-card">
        <p className="text-xs uppercase tracking-[0.2em] muted">Flagship snapshot finding</p>
        <h2 className="mt-2 text-2xl font-semibold">Where to look first, now</h2>
        <p className="mt-3 max-w-4xl text-sm muted">{FLAGSHIP_SNAPSHOT_HEADLINE}</p>
      </div>

      <div className="panel rounded-2xl p-6" data-testid="findings-persistence-card">
        <p className="text-xs uppercase tracking-[0.2em] muted">Longitudinal persistence evidence</p>
        <h3 className="mt-2 text-xl font-semibold">Flagship signal durability over deterministic snapshots</h3>
        <p className="mt-2 text-sm muted">
          Window {LONGITUDINAL_WINDOW_NAME}: dominant top market persisted in {formatPct(persistence.persistenceRate)} of
          snapshots.
        </p>
        <p className="text-sm muted">
          Average top-share: {formatPct(persistence.averageTopShare)} (range {formatPct(persistence.minTopShare)} to {formatPct(persistence.maxTopShare)}).
        </p>

        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[760px] text-sm" data-testid="persistence-table">
            <thead>
              <tr className="border-b border-slate-500/40 text-left muted">
                <th className="pb-2 pr-3">Snapshot</th>
                <th className="pb-2 pr-3">Top market</th>
                <th className="pb-2 pr-3">Top-share</th>
                <th className="pb-2 pr-3">Top-to-second</th>
                <th className="pb-2 pr-3">HHI</th>
              </tr>
            </thead>
            <tbody>
              {FLAGSHIP_PERSISTENCE_SNAPSHOTS.map((row) => (
                <tr key={row.snapshot_id} className="border-b border-slate-800/80">
                  <td className="py-3 pr-3">{row.label}</td>
                  <td className="py-3 pr-3">{row.top_market_title}</td>
                  <td className="py-3 pr-3">{formatPct(row.top_share_of_total_gap)}</td>
                  <td className="py-3 pr-3">{row.top_to_second_ratio.toFixed(3)}x</td>
                  <td className="py-3 pr-3">{row.herfindahl_index.toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="panel rounded-2xl p-6" data-testid="findings-secondary-card">
        <p className="text-xs uppercase tracking-[0.2em] muted">Secondary deterministic finding</p>
        <h3 className="mt-2 text-xl font-semibold">Platform gap asymmetry</h3>
        <p className="mt-2 text-sm muted">{SECONDARY_FINDING_ONE_SENTENCE}</p>
        <p className="text-sm muted">
          Average asymmetry: {formatPts(secondary.averageAsymmetryGap)} | Positive in {secondary.positiveWindowCount}/
          {SECONDARY_FINDING_SNAPSHOTS.length} snapshots.
        </p>

        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[760px] text-sm" data-testid="secondary-table">
            <thead>
              <tr className="border-b border-slate-500/40 text-left muted">
                <th className="pb-2 pr-3">Snapshot</th>
                <th className="pb-2 pr-3">Polymarket mean gap</th>
                <th className="pb-2 pr-3">Kalshi mean gap</th>
                <th className="pb-2 pr-3">Asymmetry</th>
              </tr>
            </thead>
            <tbody>
              {SECONDARY_FINDING_SNAPSHOTS.map((row) => (
                <tr key={row.snapshot_id} className="border-b border-slate-800/80">
                  <td className="py-3 pr-3">{row.label}</td>
                  <td className="py-3 pr-3">{formatPts(row.polymarket_mean_gap)}</td>
                  <td className="py-3 pr-3">{formatPts(row.kalshi_mean_gap)}</td>
                  <td className="py-3 pr-3">{formatPts(row.asymmetry_gap)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
