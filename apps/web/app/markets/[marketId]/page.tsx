import { notFound } from "next/navigation";

import { MarketDetail } from "@/components/market-detail";
import { DEMO_MARKETS, DEMO_MARKETS_BY_ID } from "@/lib/demo-data";

interface Props {
  params: {
    marketId: string;
  };
}

export default function MarketDetailPage({ params }: Props) {
  const detail = DEMO_MARKETS_BY_ID[params.marketId];
  if (!detail) {
    notFound();
  }

  const peers = DEMO_MARKETS.filter(
    (market) => market.category === detail.category && market.market_id !== detail.market_id
  );

  return <MarketDetail detail={detail} peerMarkets={peers} />;
}
