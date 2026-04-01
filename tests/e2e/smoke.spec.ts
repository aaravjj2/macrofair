import { expect, test } from "@playwright/test";

test("screener to detail and methodology", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByTestId("search-input")).toBeVisible();
  await expect(page.getByTestId("platform-filter")).toBeVisible();
  await expect(page.getByTestId("category-filter")).toBeVisible();
  await expect(page.getByTestId("sort-control")).toBeVisible();

  await page.getByTestId("market-table-row-poly-cpi-jun-2026-over-3").click();
  await expect(page.getByTestId("market-detail-header")).toBeVisible();
  await expect(page.getByTestId("fair-value-card")).toBeVisible();
  await expect(page.getByTestId("mispricing-score-card")).toBeVisible();
  await expect(page.getByTestId("price-history-chart")).toBeVisible();
  await expect(page.getByTestId("macro-series-chart")).toBeVisible();
  await expect(page.getByTestId("factor-contribution-panel")).toBeVisible();
  await expect(page.getByTestId("similar-setups-panel")).toBeVisible();

  await page.getByTestId("nav-methodology-link").click();
  await expect(page.getByTestId("methodology-page")).toBeVisible();
});
