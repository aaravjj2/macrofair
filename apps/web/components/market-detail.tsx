"use client";

import Link from "next/link";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { MarketDetail as MarketDetailType, MarketSummary } from "@/lib/types";

interface Props {
  detail: MarketDetailType;
  peerMarkets: MarketSummary[];
}

function pct(value: number) {
  return `${(value * 100).toFixed(1)}%`;
}

function gap(value: number) {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${(value * 100).toFixed(1)} pts`;
}

export function MarketDetail({ detail, peerMarkets }: Props) {
  return (
    <section className="space-y-6">
      <div className="panel rounded-2xl p-5" data-testid="market-detail-header">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] muted">{detail.platform} · {detail.category}</p>
            <h2 className="text-2xl font-semibold">{detail.title}</h2>
            <p className="mt-2 max-w-3xl text-sm muted">{detail.description}</p>
          </div>
          <Link
            href="/"
            className="rounded-md border border-slate-400/40 px-3 py-2 text-sm hover:border-slate-200"
            data-testid="detail-back-link"
          >
            Back to screener
          </Link>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="panel rounded-2xl p-5" data-testid="fair-value-card">
          <p className="text-sm muted">Market vs fair value</p>
          <div className="mt-2 flex items-end gap-6">
            <div>
              <p className="text-xs muted">Market</p>
              <p className="text-3xl font-bold">{pct(detail.market_probability)}</p>
            </div>
            <div>
              <p className="text-xs muted">Fair</p>
              <p className="text-3xl font-bold">{pct(detail.fair_probability)}</p>
            </div>
          </div>
        </div>
        <div className="panel rounded-2xl p-5" data-testid="mispricing-score-card">
          <p className="text-sm muted">Dislocation stats</p>
          <div className="mt-2 grid grid-cols-2 gap-3">
            <div>
              <p className="text-xs muted">Gap</p>
              <p className="text-2xl font-bold">{gap(detail.gap)}</p>
            </div>
            <div>
              <p className="text-xs muted">Confidence</p>
              <p className="text-2xl font-bold">{pct(detail.confidence)}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="panel rounded-2xl p-5" data-testid="price-history-chart">
          <p className="mb-3 text-sm muted">Market probability history</p>
          <div className="h-64">
            <ResponsiveContainer>
              <LineChart data={detail.history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#355166" />
                <XAxis dataKey="timestamp" tick={{ fontSize: 10 }} minTickGap={20} />
                <YAxis domain={[0, 1]} tickFormatter={(value) => `${Math.round(value * 100)}%`} />
                <Tooltip formatter={(value: number) => `${(value * 100).toFixed(1)}%`} />
                <Line type="monotone" dataKey="probability" stroke="#f4a259" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="panel rounded-2xl p-5" data-testid="macro-series-chart">
          <p className="mb-3 text-sm muted">Linked macro series ({detail.macro_series_id})</p>
          <div className="h-64">
            <ResponsiveContainer>
              <LineChart data={detail.linked_macro_series}>
                <CartesianGrid strokeDasharray="3 3" stroke="#355166" />
                <XAxis dataKey="timestamp" tick={{ fontSize: 10 }} minTickGap={20} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#6ed39e" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="panel rounded-2xl p-5" data-testid="factor-contribution-panel">
          <p className="text-sm muted">Explanation factors</p>
          <p className="mt-2 text-sm">{detail.explanation.narrative_summary}</p>
          <ul className="mt-3 space-y-2 text-sm">
            {Object.entries(detail.explanation.factor_contributions).map(([factor, value]) => (
              <li key={factor} className="flex items-center justify-between rounded-md border border-slate-500/30 px-3 py-2">
                <span>{factor.replaceAll("_", " ")}</span>
                <strong>{value >= 0 ? "+" : ""}{value.toFixed(3)}</strong>
              </li>
            ))}
          </ul>
        </div>
        <div className="panel rounded-2xl p-5" data-testid="similar-setups-panel">
          <p className="text-sm muted">Similar setups</p>
          <div className="mt-3 space-y-2 text-sm">
            {peerMarkets.map((peer) => (
              <div key={peer.market_id} className="rounded-md border border-slate-500/30 px-3 py-2">
                <p className="font-medium">{peer.title}</p>
                <p className="muted">Gap {gap(peer.gap)} · Confidence {pct(peer.confidence)}</p>
                <Link
                  href={`/markets/${peer.market_id}`}
                  className="mt-2 inline-block rounded-md border border-slate-400/40 px-2 py-1 text-xs hover:border-slate-200"
                  data-testid={`similar-link-${peer.market_id}`}
                >
                  Open
                </Link>
              </div>
            ))}
            {peerMarkets.length === 0 && <p className="muted">No similar setups found in this demo snapshot.</p>}
          </div>
        </div>
      </div>
    </section>
  );
}
