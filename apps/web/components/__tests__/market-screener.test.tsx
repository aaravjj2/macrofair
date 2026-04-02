import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ReactNode } from "react";
import { describe, expect, it, vi } from "vitest";

import { MarketScreener } from "@/components/market-screener";
import { DEMO_MARKETS } from "@/lib/demo-data";

vi.mock("next/link", () => ({
  default: ({ href, children, ...props }: { href: string; children: ReactNode }) => (
    <a href={href} {...props}>
      {children}
    </a>
  )
}));

describe("MarketScreener", () => {
  it("renders completed state and allows filtering", async () => {
    const user = userEvent.setup();
    render(<MarketScreener markets={DEMO_MARKETS} />);

    await waitFor(() => expect(screen.getByTestId("state-completed")).toBeInTheDocument());
    expect(screen.getByTestId("hero-section")).toBeInTheDocument();
    expect(screen.getByTestId("flagship-finding-card")).toBeInTheDocument();
    expect(screen.getByTestId("market-table")).toBeInTheDocument();

    await user.selectOptions(screen.getByTestId("platform-filter"), "Kalshi");
    await waitFor(() => expect(screen.getByText(/Fed cuts target rate/i)).toBeInTheDocument());
  });
});
