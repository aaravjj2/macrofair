# Project Brief

## Product

**MacroFair**

## Problem

Prediction markets are useful aggregators of information, but live prices are not always well calibrated to observable macro fundamentals. Traders and observers can see the crowd price, but they usually cannot see:
- how far that price is from a fundamentals-aware estimate
- whether similar divergences historically mean-reverted
- how much trust to place in the divergence given liquidity and horizon

## Solution

MacroFair is a live screener and API for macro prediction markets. It:
1. ingests live Polymarket and Kalshi contracts
2. maps each contract to a macro event or economic variable
3. estimates a fair-value probability from macro features and historical behavior
4. scores the gap between market-implied probability and fair value
5. explains the main drivers behind each disagreement

## Primary user

Hackathon judges first, then:
- macro hobbyists
- prediction-market analysts
- researchers studying calibration
- traders looking for structured dislocation signals

## Core question

When do macro prediction-market prices diverge from fundamentals, and do similar divergences historically close?

## V1 scope

Start with contracts about:
- CPI / inflation
- Fed decisions
- unemployment
- recession
- GDP / macro release bands

## Non-goals for V1

- autonomous trading
- auto-submitting orders
- supporting every market category
- portfolio management
- PnL-heavy optimization

## Product outputs

### User-facing app
- ranked screener of live dislocations
- market detail page with explanation
- charts for price, fundamentals, and fair value
- cross-platform comparison when available

### API
- ranked dislocations
- market explanation endpoint
- snapshot endpoint
- health + metadata endpoints

### Research outputs
- calibration report
- feature importance / explanation report
- backtest summary
- demo-ready charts

## Why it can win

- strong analytical story
- visible end-to-end workflow
- live deployed output
- clear value without needing execution risk
