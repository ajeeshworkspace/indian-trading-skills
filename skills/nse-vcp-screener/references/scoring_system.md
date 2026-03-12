# VCP Composite Scoring System

## Overview

The composite score (0-100) combines five independent components, each measuring a different aspect of VCP quality. Higher scores indicate more textbook-like setups with better risk/reward characteristics.

## Component Weights

| # | Component | Weight | What It Measures |
|---|-----------|--------|-----------------|
| 1 | Trend Template | 25% | Minervini's 7-point Stage 2 criteria |
| 2 | Contraction Quality | 25% | Tightening base structure |
| 3 | Volume Pattern | 20% | Volume dry-up signature |
| 4 | Pivot Proximity | 15% | Distance from breakout level |
| 5 | Relative Strength | 15% | Performance vs Nifty 50 |

```
Composite Score = (Trend × 0.25) + (Contraction × 0.25) + (Volume × 0.20) + (Pivot × 0.15) + (RS × 0.15)
```

## Component 1: Trend Template Score (0-100)

Based on Minervini's 7-point criteria. Each criterion = ~14.3 points.

| Criteria Met | Score |
|-------------|-------|
| 7/7 | 100 |
| 6/7 | 85 |
| 5/7 | 71 |
| < 5/7 | Disqualified |

**Minimum threshold**: 85 (6/7 criteria). Stocks scoring below this are eliminated in Phase 2.

## Component 2: Contraction Quality Score (0-100)

Evaluates the structure and cleanliness of price contractions.

### Base Score

| Pattern | Base Score |
|---------|-----------|
| 4+ clean contractions | 80-90 |
| 3 clean contractions | 65-80 |
| 2 clean contractions | 50-65 |

### Modifiers

| Condition | Modifier |
|-----------|----------|
| Consistent contraction ratio < 0.60 | +10 |
| Final contraction depth < 5% | +10 |
| T1 depth in ideal range (15-30%) | +5 |
| Irregular/overlapping contractions | -15 to -25 |
| T1 too shallow (< 10%) | -10 |
| T1 too deep (> 40%) | -15 |

## Component 3: Volume Pattern Score (0-100)

Based on the volume dry-up ratio (recent 10-day avg / 50-day avg).

| Dry-Up Ratio | Score |
|--------------|-------|
| < 0.40 | 90 |
| 0.40-0.50 | 80 |
| 0.50-0.60 | 70 |
| 0.60-0.70 | 60 |
| 0.70-0.80 | 45 |
| 0.80-0.90 | 30 |
| > 0.90 | 15 |

## Component 4: Pivot Proximity Score (0-100)

Measures how close the current price is to the breakout pivot level.

| Distance from Pivot | Score |
|--------------------|-------|
| 0-3% below pivot | 90 |
| 3-5% below pivot | 75 |
| 5-8% below pivot | 60 |
| 8-12% below pivot | 45 |
| 12-20% below pivot | 30 |
| > 20% below pivot | 15 |
| Above pivot (already broken out) | 50 (late entry risk) |

## Component 5: Relative Strength Score (0-100)

Measures stock's performance vs Nifty 50 using Minervini-weighted formula.

```
RS = 0.40 × (3-month return vs Nifty) + 0.20 × (6-month return vs Nifty) + 0.20 × (9-month return vs Nifty) + 0.20 × (12-month return vs Nifty)
```

| RS Value | Score |
|----------|-------|
| > 50% outperformance | 95 |
| 30-50% | 80 |
| 15-30% | 65 |
| 5-15% | 50 |
| 0-5% | 35 |
| < 0% (underperforming) | 15 |

## Interpreting Composite Scores

| Score Range | Quality | Action |
|-------------|---------|--------|
| 80-100 | Excellent | High conviction setup — prepare entry plan |
| 65-79 | Good | Watchlist — monitor for pivot approach |
| 50-64 | Fair | Early stage or flawed pattern — check individual components |
| < 50 | Poor | Not a valid VCP — skip |

## Example Scoring

**Stock: PERSISTENT (NSE)**

| Component | Raw Score | Weight | Weighted |
|-----------|----------|--------|----------|
| Trend Template (7/7) | 100 | 25% | 25.0 |
| Contraction Quality (3 contractions, ratio 0.55) | 80 | 25% | 20.0 |
| Volume Dry-Up (ratio 0.48) | 80 | 20% | 16.0 |
| Pivot Proximity (2.5% below) | 90 | 15% | 13.5 |
| Relative Strength (RS = 32%) | 80 | 15% | 12.0 |
| **Composite** | | | **86.5** |

Verdict: Excellent setup — prepare entry plan with stop below final contraction low.
