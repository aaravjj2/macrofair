import { expect, test } from "@playwright/test";

test("screener to detail and methodology", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByTestId("hero-section")).toBeVisible();
  await expect(page.getByTestId("hero-featured-dislocation")).toBeVisible();
  await expect(page.getByTestId("flagship-finding-card")).toBeVisible();

  await expect(page.getByTestId("search-input")).toBeVisible();
  await expect(page.getByTestId("platform-filter")).toBeVisible();
  await expect(page.getByTestId("category-filter")).toBeVisible();
  await expect(page.getByTestId("sort-control")).toBeVisible();

  await page.getByTestId("hero-featured-link").click();
  await expect(page.getByTestId("market-detail-header")).toBeVisible();
  await expect(page.getByTestId("market-context-grid")).toBeVisible();
  await expect(page.getByTestId("fair-value-card")).toBeVisible();
  await expect(page.getByTestId("mispricing-score-card")).toBeVisible();
  await expect(page.getByTestId("price-history-chart")).toBeVisible();
  await expect(page.getByTestId("macro-series-chart")).toBeVisible();
  await expect(page.getByTestId("factor-contribution-panel")).toBeVisible();
  await expect(page.getByTestId("similar-setups-panel")).toBeVisible();
  await expect(page.getByTestId("detail-interpretation-panel")).toBeVisible();

  await page.getByTestId("detail-methodology-link").click();
  await expect(page.getByTestId("methodology-interpretation-section")).toBeVisible();
  await expect(page.getByTestId("methodology-findings-evidence")).toBeVisible();

  await page.getByTestId("methodology-findings-link").click();
  await expect(page.getByTestId("findings-page")).toBeVisible();
  await expect(page.getByTestId("findings-snapshot-card")).toBeVisible();
  await expect(page.getByTestId("findings-zerve-status-card")).toBeVisible();
  await expect(page.getByTestId("findings-zerve-status-enabled")).toBeVisible();
  await expect(page.getByTestId("findings-zerve-status-configured")).toBeVisible();
  await expect(page.getByTestId("findings-persistence-card")).toBeVisible();
  await expect(page.getByTestId("findings-secondary-card")).toBeVisible();
  await expect(page.getByTestId("findings-third-card")).toBeVisible();
  await expect(page.getByTestId("persistence-table")).toBeVisible();
  await expect(page.getByTestId("secondary-table")).toBeVisible();
  await expect(page.getByTestId("third-table")).toBeVisible();

  await page.getByTestId("nav-home-link").click();
  await expect(page.getByTestId("market-table")).toBeVisible();
});
