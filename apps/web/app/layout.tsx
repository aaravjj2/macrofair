import type { Metadata } from "next";
import { TopNav } from "@/components/top-nav";

import "./globals.css";

export const metadata: Metadata = {
  title: "MacroFair",
  description: "Macro market mispricing screener"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div className="mx-auto max-w-7xl px-4 py-6 md:px-6">
          <TopNav />
          {children}
        </div>
      </body>
    </html>
  );
}
