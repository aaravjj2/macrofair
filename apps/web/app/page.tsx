import { MarketScreener } from "@/components/market-screener";
import { DEMO_MARKETS } from "@/lib/demo-data";

export default function HomePage() {
  return <MarketScreener markets={DEMO_MARKETS} />;
}
