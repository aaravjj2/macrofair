# Frontend Design

## Frontend objective

Make the product instantly understandable within 15 seconds:
- show what the market thinks
- show what MacroFair thinks
- show the gap
- show why

## Design principles

- Decision support, not clutter
- Table-first, explanation-second
- Every number must have provenance
- Every interactive element must have `data-testid`
- Empty, loading, error, and completed states for every panel

## Tech stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- shadcn/ui
- Recharts
- Framer Motion only if disabled in E2E mode

## Information architecture

### 1. Home / Screener
Purpose: rank the most interesting live dislocations.

Components:
- top nav
- market filters
- metric summary strip
- main data table
- selected market insight side panel

Columns:
- contract
- platform
- category
- market probability
- fair probability
- gap
- confidence
- liquidity quality
- hours to resolution
- last updated

Top actions:
- search
- filter by platform
- filter by category
- sort by gap / confidence / time
- open details

### 2. Market detail page
Purpose: prove the score is real.

Sections:
- contract header
- market vs fair value headline stats
- time-series chart
- factor contribution / explanation
- liquidity and spread panel
- related macro series chart
- similar historical setups
- methodology footer

### 3. Methodology page
Purpose: build judge trust.

Sections:
- how fair value is estimated
- what mispricing means
- limitations
- evaluation metrics
- data sources

### 4. About / Demo page
Purpose: help judges quickly understand the story.

Sections:
- problem
- workflow
- key findings
- screenshots / embedded demo video

## Visual language

Tone:
- serious, analytical, clean
- no meme finance aesthetic
- no neon trading terminal look

Patterns:
- cards with rounded corners
- restrained color use
- clear typography hierarchy
- simple sparklines / line charts
- badges for platform and category

## Key components and test IDs

- `data-testid="market-table"`
- `data-testid="market-table-row-{id}"`
- `data-testid="search-input"`
- `data-testid="platform-filter"`
- `data-testid="category-filter"`
- `data-testid="sort-control"`
- `data-testid="market-detail-header"`
- `data-testid="fair-value-card"`
- `data-testid="mispricing-score-card"`
- `data-testid="price-history-chart"`
- `data-testid="macro-series-chart"`
- `data-testid="factor-contribution-panel"`
- `data-testid="similar-setups-panel"`

## States

Every major panel must support:
- empty
- loading
- working
- completed
- error

## Accessibility and E2E safety

- keyboard navigable controls
- no hover-only actions
- all charts render headless
- animations disabled in E2E mode
- deterministic snapshot data for demo mode

## First-screen success criterion

A judge lands on the home page and can say:
"This shows live macro markets, compares crowd odds to a fair-value estimate, and ranks the biggest disagreements."
