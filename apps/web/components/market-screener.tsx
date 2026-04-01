"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { DEMO_METADATA } from "@/lib/demo-data";
import { filterAndSortMarkets, MarketSort } from "@/lib/market-utils";
import { MarketSummary } from "@/lib/types";

type PanelState = "loading" | "working" | "completed" | "empty" | "error";

interface Props {
  markets: MarketSummary[];
}

function formatPct(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

function formatGap(value: number): string {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${(value * 100).toFixed(1)} pts`;
}

export function MarketScreener({ markets }: Props) {
  const [search, setSearch] = useState("");
  const [platform, setPlatform] = useState("all");
  const [category, setCategory] = useState("all");
  const [sortBy, setSortBy] = useState<MarketSort>("gap");
  const [isLoading, setIsLoading] = useState(true);
  const [isWorking, setIsWorking] = useState(false);
  const [loadError] = useState<string | null>(null);

  useEffect(() => {
    const timerId = window.setTimeout(() => setIsLoading(false), 220);
    return () => window.clearTimeout(timerId);
  }, []);

  useEffect(() => {
    if (isLoading) {
      return;
    }

    setIsWorking(true);
    const timerId = window.setTimeout(() => setIsWorking(false), 120);
    return () => window.clearTimeout(timerId);
  }, [search, platform, category, sortBy]);

  const filteredMarkets = useMemo(
    () =>
      filterAndSortMarkets(markets, {
        search,
        platform,
        category,
        sortBy
      }),
    [markets, search, platform, category, sortBy]
  );

  const panelState: PanelState = loadError
    ? "error"
    : isLoading
      ? "loading"
      : isWorking
        ? "working"
        : filteredMarkets.length === 0
          ? "empty"
          : "completed";

  const spotlight = filteredMarkets[0];

  return (
    <section className="space-y-6">
      <div className="panel rounded-2xl p-5" data-testid="summary-strip">
        <p className="text-xs uppercase tracking-[0.2em] muted">Deterministic demo mode</p>
        <div className="mt-2 grid gap-3 text-sm md:grid-cols-3">
          <div>
            <p className="muted">Markets tracked</p>
            <p className="text-xl font-semibold">{markets.length}</p>
          </div>
          <div>
            <p className="muted">Last refresh</p>
            <p className="font-medium">{new Date(DEMO_METADATA.last_refresh).toUTCString()}</p>
          </div>
          <div>
            <p className="muted">Model version</p>
            <p className="font-medium">{DEMO_METADATA.model_version}</p>
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <div className="panel rounded-2xl p-5">
          <div className="mb-4 grid gap-3 md:grid-cols-4">
            <label className="text-sm">
              <span className="mb-1 block muted">Search</span>
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search contract"
                className="w-full rounded-md border border-slate-500/50 bg-transparent px-3 py-2"
                data-testid="search-input"
              />
            </label>
            <label className="text-sm">
              <span className="mb-1 block muted">Platform</span>
              <select
                value={platform}
                onChange={(event) => setPlatform(event.target.value)}
                className="w-full rounded-md border border-slate-500/50 bg-[#0a1d2c] px-3 py-2"
                data-testid="platform-filter"
              >
                <option value="all">All</option>
                <option value="Polymarket">Polymarket</option>
                <option value="Kalshi">Kalshi</option>
              </select>
            </label>
            <label className="text-sm">
              <span className="mb-1 block muted">Category</span>
              <select
                value={category}
                onChange={(event) => setCategory(event.target.value)}
                className="w-full rounded-md border border-slate-500/50 bg-[#0a1d2c] px-3 py-2"
                data-testid="category-filter"
              >
                <option value="all">All</option>
                <option value="inflation">Inflation</option>
                <option value="fed">Fed</option>
                <option value="unemployment">Unemployment</option>
                <option value="recession">Recession</option>
                <option value="gdp">GDP</option>
              </select>
            </label>
            <label className="text-sm">
              <span className="mb-1 block muted">Sort</span>
              <select
                value={sortBy}
                onChange={(event) => setSortBy(event.target.value as MarketSort)}
                className="w-full rounded-md border border-slate-500/50 bg-[#0a1d2c] px-3 py-2"
                data-testid="sort-control"
              >
                <option value="gap">Gap</option>
                <option value="confidence">Confidence</option>
                <option value="time">Time to resolution</option>
              </select>
            </label>
          </div>

          <div className="mb-4 text-sm" data-testid="panel-state">
            <span className="inline-flex rounded-full border border-slate-400/40 px-3 py-1 uppercase tracking-[0.15em]">
              {panelState}
            </span>
          </div>

          {panelState === "error" && (
            <div className="rounded-xl border border-red-300/30 bg-red-900/20 p-4" data-testid="state-error">
              Failed to load data.
            </div>
          )}
          {(panelState === "loading" || panelState === "working") && (
            <div className="rounded-xl border border-slate-300/30 bg-slate-900/30 p-4" data-testid="state-loading">
              Syncing deterministic snapshot...
            </div>
          )}
          {panelState === "empty" && (
            <div className="rounded-xl border border-slate-300/30 bg-slate-900/30 p-4" data-testid="state-empty">
              No contracts match this filter set.
            </div>
          )}

          {panelState === "completed" && (
            <div className="overflow-x-auto" data-testid="state-completed">
              <table className="w-full min-w-[860px] text-sm" data-testid="market-table">
                <thead>
                  <tr className="border-b border-slate-500/40 text-left muted">
                    <th className="pb-2 pr-3">Contract</th>
                    <th className="pb-2 pr-3">Platform</th>
                    <th className="pb-2 pr-3">Market Prob.</th>
                    <th className="pb-2 pr-3">Fair Prob.</th>
                    <th className="pb-2 pr-3">Gap</th>
                    <th className="pb-2 pr-3">Confidence</th>
                    <th className="pb-2 pr-3">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredMarkets.map((market) => (
                    <tr key={market.market_id} className="border-b border-slate-800/80">
                      <td className="py-3 pr-3 font-medium">{market.title}</td>
                      <td className="py-3 pr-3">{market.platform}</td>
                      <td className="py-3 pr-3">{formatPct(market.market_probability)}</td>
                      <td className="py-3 pr-3">{formatPct(market.fair_probability)}</td>
                      <td
                        className={`py-3 pr-3 ${market.gap >= 0 ? "text-[#ffd3a7]" : "text-[#9fe2c0]"}`}
                      >
                        {formatGap(market.gap)}
                      </td>
                      <td className="py-3 pr-3">{formatPct(market.confidence)}</td>
                      <td className="py-3 pr-3">
                        <Link
                          href={`/markets/${market.market_id}`}
                          className="rounded-md border border-slate-400/40 px-2 py-1 text-xs hover:border-slate-200"
                          data-testid={`market-table-row-${market.market_id}`}
                        >
                          Open details
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <aside className="panel rounded-2xl p-5" data-testid="market-insight-panel">
          <p className="text-xs uppercase tracking-[0.2em] muted">Selected market insight</p>
          {spotlight ? (
            <div className="mt-3 space-y-2 text-sm">
              <h2 className="text-base font-semibold leading-tight">{spotlight.title}</h2>
              <p className="muted">{spotlight.platform} · {spotlight.category}</p>
              <div className="grid grid-cols-2 gap-2 pt-2">
                <div className="rounded-lg border border-slate-500/30 p-2">
                  <p className="text-xs muted">Market</p>
                  <p className="font-semibold">{formatPct(spotlight.market_probability)}</p>
                </div>
                <div className="rounded-lg border border-slate-500/30 p-2">
                  <p className="text-xs muted">Fair</p>
                  <p className="font-semibold">{formatPct(spotlight.fair_probability)}</p>
                </div>
                <div className="rounded-lg border border-slate-500/30 p-2">
                  <p className="text-xs muted">Gap</p>
                  <p className="font-semibold">{formatGap(spotlight.gap)}</p>
                </div>
                <div className="rounded-lg border border-slate-500/30 p-2">
                  <p className="text-xs muted">Confidence</p>
                  <p className="font-semibold">{formatPct(spotlight.confidence)}</p>
                </div>
              </div>
            </div>
          ) : (
            <p className="mt-3 text-sm muted">Adjust filters to inspect a market.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
