# Breadth Analysis Methodology — Indian Markets (NSE/BSE)

## Table of Contents

1. [What Market Breadth Means for NSE](#what-market-breadth-means-for-nse)
2. [Core Breadth Indicators](#core-breadth-indicators)
3. [Composite Score Calculation](#composite-score-calculation)
4. [Divergence Detection](#divergence-detection)
5. [Using Breadth to Time Equity Allocation](#using-breadth-to-time-equity-allocation)
6. [Historical Case Studies](#historical-case-studies)
7. [India-Specific Considerations](#india-specific-considerations)

---

## What Market Breadth Means for NSE

### The NSE Universe

The National Stock Exchange of India has approximately 1,800-2,000 actively traded stocks on any given day. The key indices, however, represent only a small fraction:

| Index | Stocks | Market Cap Coverage |
|-------|--------|-------------------|
| Nifty 50 | 50 | ~62% of NSE market cap |
| Nifty 100 | 100 | ~76% of NSE market cap |
| Nifty 200 | 200 | ~85% of NSE market cap |
| Nifty 500 | 500 | ~93% of NSE market cap |
| Nifty Total Market | 750+ | ~96% of NSE market cap |
| All listed stocks | 1,800+ | 100% |

### Why Breadth Matters

The Nifty 50 is market-cap weighted. The top 10 stocks (Reliance, TCS, HDFC Bank, Infosys, ICICI Bank, etc.) account for approximately 45-50% of the index weight. This means:

- Nifty can rise 1% even if 40 of the 50 stocks are flat or down, as long as the top 10 are up
- A Nifty rally driven by just 5-10 heavyweight stocks is fragile
- When these heavyweights stall, the index reverses sharply

**Breadth answers the question: "Is the MARKET going up, or just a few big stocks?"**

### Healthy vs Narrow Markets

| Characteristic | Healthy (Broad) Market | Narrow (Fragile) Market |
|---------------|----------------------|----------------------|
| A/D ratio | > 1.5:1 | < 1.0:1 |
| % above 200 DMA | > 60% | < 40% |
| New highs vs lows | > 2:1 | < 1:1 |
| Sectors participating | 8+ of 13 | < 5 of 13 |
| Cap-tier alignment | Large, mid, small all up | Only large-cap up |
| Typical duration | Months to years | Weeks to months |
| Risk of reversal | Low | High |

---

## Core Breadth Indicators

### 1. Advance/Decline (A/D) Ratio

The most fundamental breadth indicator. Simply count how many stocks went up versus down on a given day.

#### Calculation
```
A/D Ratio = Number of Advancing Stocks / Number of Declining Stocks

Example: 1,100 advances / 650 declines = 1.69
```

#### Interpretation for NSE

| A/D Ratio | Market Condition | Signal |
|-----------|-----------------|--------|
| > 3.0 | Extreme broad rally | Very bullish, but may be overbought short-term |
| 2.0 - 3.0 | Strong broad rally | Bullish, healthy participation |
| 1.5 - 2.0 | Healthy rally | Normal bullish condition |
| 1.2 - 1.5 | Mild bullish | Slightly positive, nothing conclusive |
| 1.0 - 1.2 | Neutral | Mixed market, no clear direction |
| 0.7 - 1.0 | Mild bearish | More stocks declining than advancing |
| 0.5 - 0.7 | Broad selling | Bearish, widespread decline |
| < 0.5 | Panic/capitulation | Very bearish, but may signal bottom |

#### Smoothing

Use the 5-day simple moving average of the A/D ratio to filter daily noise. The 20-day SMA shows the medium-term trend.

- **5-day SMA rising:** Short-term breadth improving
- **5-day SMA falling:** Short-term breadth deteriorating
- **20-day SMA above 1.3:** Medium-term breadth is healthy
- **20-day SMA below 0.8:** Medium-term breadth is weak

#### A/D Line (Cumulative)

The cumulative A/D Line tracks the running total of (advances - declines) over time:
```
A/D Line(today) = A/D Line(yesterday) + (Advances - Declines)
```

The absolute value does not matter — the direction does:
- **Rising A/D Line:** Breadth expanding — bullish
- **Falling A/D Line:** Breadth contracting — bearish
- **A/D Line diverging from Nifty:** Warning signal (see Divergence section)

#### McClellan Oscillator (NSE Adaptation)

The McClellan Oscillator applies exponential smoothing to the daily advance-decline difference:
```
A/D Difference = Advances - Declines
19-day EMA of A/D Difference (fast)
39-day EMA of A/D Difference (slow)
McClellan Oscillator = 19-day EMA - 39-day EMA

Interpretation:
  > 0:  Bullish breadth momentum
  < 0:  Bearish breadth momentum
  > +50: Overbought breadth (potential pullback)
  < -50: Oversold breadth (potential bounce)
  Zero-line crossover: Significant momentum shift
```

### 2. Percentage of Stocks Above Moving Averages

This indicator shows what fraction of the universe is in an uptrend at various timeframes.

#### % Above 200 DMA (Long-Term Breadth)

The 200-day moving average is the standard long-term trend filter. A stock above its 200 DMA is in a long-term uptrend.

| % Above 200 DMA | Interpretation | NSE Context |
|------------------|---------------|-------------|
| > 75% | Extreme broad participation | Very rare, typically early-to-mid bull market |
| 60-75% | Broad participation | Healthy bull market, most stocks in uptrend |
| 50-60% | Moderate participation | Market is positive but not uniformly |
| 40-50% | Selective market | Only certain sectors/themes working |
| 30-40% | Narrow market | Most stocks in downtrend, index propped by few |
| < 30% | Bear market breadth | Broad-based decline, most stocks below long-term average |
| < 15% | Capitulation zone | Extreme pessimism, historically near bottoms |

**Key thresholds for action:**
- **Above 60%:** Maintain full equity exposure, broad-based strategies work
- **Below 40%:** Reduce exposure, focus on relative strength leaders only
- **Below 25%:** Maximum defense OR contrarian accumulation zone

#### % Above 50 DMA (Medium-Term Breadth)

The 50-day moving average captures medium-term trends. This indicator is more sensitive and turns earlier than the 200 DMA breadth.

| % Above 50 DMA | Interpretation |
|-----------------|---------------|
| > 65% | Strong medium-term breadth |
| 45-65% | Normal/healthy |
| 30-45% | Weakening |
| < 30% | Oversold, potential mean reversion |

**Cross-reading with 200 DMA:**
- % above 200 DMA high BUT % above 50 DMA falling = Medium-term weakness developing within a longer-term uptrend (early warning)
- % above 200 DMA low BUT % above 50 DMA rising = Potential trend reversal forming (early bullish signal)

### 3. New 52-Week Highs vs New 52-Week Lows

This is one of the most powerful breadth indicators. It measures momentum by counting how many stocks are at their strongest (or weakest) levels in a year.

#### Calculation
```
New 52W Highs = Count of stocks where today's high >= highest high in prior 252 trading days
New 52W Lows = Count of stocks where today's low <= lowest low in prior 252 trading days
NH-NL Differential = New Highs - New Lows
New Highs Ratio = New Highs / (New Highs + New Lows)
```

#### Interpretation

| Ratio (Highs / (Highs+Lows)) | Signal |
|-------------------------------|--------|
| > 0.80 (>4:1 ratio) | Strong bullish breadth, broad momentum |
| 0.60 - 0.80 | Healthy breadth, more strength than weakness |
| 0.40 - 0.60 | Neutral / transitioning |
| 0.20 - 0.40 | Bearish breadth, weakness spreading |
| < 0.20 (>4:1 lows ratio) | Strong bearish breadth, broad weakness |

#### NSE-Specific Observations

On a typical day in the Indian market:
- **Healthy bull market:** 80-150+ new highs, 10-30 new lows
- **Neutral market:** 30-60 new highs, 20-40 new lows
- **Bear market:** 5-20 new highs, 60-200+ new lows
- **Capitulation:** 0-5 new highs, 200-400+ new lows

**Important:** Compare the number of new highs at each Nifty peak. If Nifty makes a higher high but new highs are fewer than at the previous peak, breadth is diverging negatively.

### 4. Sector Participation

Market rallies that are driven by multiple sectors are more sustainable than those concentrated in one or two sectors.

#### The 13 Key NSE Sectors

| # | Sector Index | Key Stocks | Macro Sensitivity |
|---|-------------|------------|-------------------|
| 1 | Nifty Bank | HDFC Bank, ICICI Bank, SBI, Kotak | Interest rates, credit growth |
| 2 | Nifty IT | TCS, Infosys, Wipro, HCL Tech | USD/INR, US demand, tech spending |
| 3 | Nifty Pharma | Sun Pharma, Dr Reddy's, Cipla | USFDA approvals, US generics |
| 4 | Nifty FMCG | HUL, ITC, Nestle, Britannia | Rural demand, monsoon, inflation |
| 5 | Nifty Auto | M&M, Maruti, Tata Motors, Bajaj Auto | Consumer spending, EV transition |
| 6 | Nifty Metal | Tata Steel, JSW Steel, Hindalco | Global commodity cycle, China |
| 7 | Nifty Realty | DLF, Godrej Properties, Oberoi | Interest rates, housing demand |
| 8 | Nifty Energy | Reliance, NTPC, Power Grid, ONGC | Crude oil, government policy |
| 9 | Nifty Infra | L&T, Adani Ports, UltraTech | Government capex, budget allocation |
| 10 | Nifty PSU Bank | SBI, Bank of Baroda, PNB, Canara | NPA cycle, government recapitalization |
| 11 | Nifty Pvt Bank | HDFC Bank, ICICI Bank, Kotak, Axis | Credit growth, asset quality |
| 12 | Nifty Media | Zee, PVR Inox, Sun TV, TV18 | Ad spending, digital transition |
| 13 | Nifty Fin Service | Bajaj Finance, SBI Life, HDFC AMC | Credit cycle, insurance penetration |

#### Measuring Sector Participation

For each sector, determine if it is in an "uptrend" by checking:
1. **Sector index above its 50 DMA** — Primary criterion
2. **Positive 1-month return** — Secondary criterion
3. **Positive 3-month return** — Confirmation

A sector is "participating" if at least 2 of the 3 criteria are met.

#### Interpretation

| Sectors Participating | Market Health |
|----------------------|---------------|
| 11-13 out of 13 | Broad rally — extremely healthy |
| 8-10 out of 13 | Healthy rally — normal bull market |
| 6-7 out of 13 | Selective rally — some caution warranted |
| 4-5 out of 13 | Narrow rally — high risk |
| 0-3 out of 13 | Bear market or extreme selectivity |

#### Sector Rotation Patterns in India

Understanding which sectors lead and lag helps assess where we are in the market cycle:

```
Early Recovery:  Banks, Financials, Real Estate -> rate-sensitive recovery
Mid Expansion:   IT, Pharma, FMCG -> broad participation, earnings growth
Late Expansion:  Metals, Infrastructure, PSU -> cyclical and speculative themes
Early Downturn:  IT and FMCG outperform (defensive), cyclicals crack
Deep Downturn:   Everything falls, correlation goes to 1
Bottoming:       Banks lead again, followed by auto and consumer discretionary
```

---

## Composite Score Calculation

### 5-Component Scoring Model (Total: 100 Points)

The composite score combines all five breadth dimensions into a single number.

| # | Component | Weight | Max Points | Primary Data Source |
|---|-----------|--------|------------|-------------------|
| 1 | Advance/Decline Ratio | 25% | 25 | NSE A/D data (via web search) |
| 2 | Stocks Above 200 DMA | 25% | 25 | Screener data (via web search) |
| 3 | New Highs vs Lows | 20% | 20 | Groww MCP YEARLY_HIGH/LOW |
| 4 | Sector Participation | 15% | 15 | Sector index LTP via Groww MCP |
| 5 | Nifty Divergence | 15% | 15 | Nifty vs breadth comparison |

### Component 1: A/D Ratio Score (0-25 points)

```
If AD_ratio >= 3.0:     score = 25
If 2.5 <= AD < 3.0:     score = 22 + (AD - 2.5) / 0.5 * 3
If 2.0 <= AD < 2.5:     score = 19 + (AD - 2.0) / 0.5 * 3
If 1.5 <= AD < 2.0:     score = 15 + (AD - 1.5) / 0.5 * 4
If 1.2 <= AD < 1.5:     score = 12 + (AD - 1.2) / 0.3 * 3
If 1.0 <= AD < 1.2:     score = 8 + (AD - 1.0) / 0.2 * 4
If 0.7 <= AD < 1.0:     score = 4 + (AD - 0.7) / 0.3 * 4
If 0.5 <= AD < 0.7:     score = 2 + (AD - 0.5) / 0.2 * 2
If AD < 0.5:            score = AD / 0.5 * 2

Trend adjustment:
  If 5-day SMA of AD is rising: +2 bonus (capped at 25)
  If 5-day SMA of AD is falling: -2 penalty (floored at 0)
```

### Component 2: % Above 200 DMA Score (0-25 points)

```
If pct >= 75:          score = 25
If 65 <= pct < 75:     score = 21 + (pct - 65) / 10 * 4
If 55 <= pct < 65:     score = 17 + (pct - 55) / 10 * 4
If 45 <= pct < 55:     score = 13 + (pct - 45) / 10 * 4
If 35 <= pct < 45:     score = 9 + (pct - 35) / 10 * 4
If 25 <= pct < 35:     score = 5 + (pct - 25) / 10 * 4
If pct < 25:           score = pct / 25 * 5
```

### Component 3: New Highs vs Lows Score (0-20 points)

```
ratio = new_highs / (new_highs + new_lows)  [0 to 1]

If ratio >= 0.83 (5:1):    score = 20
If 0.75 <= ratio < 0.83:   score = 16 + (ratio - 0.75) / 0.08 * 4
If 0.67 <= ratio < 0.75:   score = 12 + (ratio - 0.67) / 0.08 * 4
If 0.50 <= ratio < 0.67:   score = 8 + (ratio - 0.50) / 0.17 * 4
If 0.33 <= ratio < 0.50:   score = 4 + (ratio - 0.33) / 0.17 * 4
If ratio < 0.33:           score = ratio / 0.33 * 4
```

### Component 4: Sector Participation Score (0-15 points)

```
sectors_up = number of sectors in uptrend (out of 13)

If sectors_up >= 11:      score = 15
If sectors_up >= 9:       score = 12 + (sectors_up - 9) / 2 * 3
If sectors_up >= 7:       score = 9 + (sectors_up - 7) / 2 * 3
If sectors_up >= 5:       score = 6 + (sectors_up - 5) / 2 * 3
If sectors_up >= 3:       score = 3 + (sectors_up - 3) / 2 * 3
If sectors_up < 3:        score = sectors_up
```

### Component 5: Nifty Divergence Score (0-15 points)

This is a qualitative component assigned based on the alignment (or divergence) of Nifty trend direction with overall breadth trend:

| Nifty Trend | Breadth Trend | Score | Label |
|-------------|---------------|-------|-------|
| Rising | Improving | 15 | Confirmed uptrend |
| Flat | Improving | 13 | Stealth accumulation |
| Rising | Flat | 10 | Narrow rally — watch closely |
| Flat | Flat | 8 | Neutral — no signal |
| Falling | Improving | 7 | Possible bottom formation |
| Flat | Declining | 5 | Stealth distribution |
| Rising | Declining | 3 | BEARISH DIVERGENCE — high risk |
| Falling | Declining | 2 | Confirmed downtrend |

### Final Score

```
Composite Score = Component1 + Component2 + Component3 + Component4 + Component5

Range: 0-100
Round to nearest integer
```

### Score Trend

Compare the current composite score to the score from 5 trading days ago:

```
Score Delta = Current Score - Score 5 days ago
```

| Delta | Trend Label |
|-------|-------------|
| > +5 | Improving |
| -5 to +5 | Stable |
| < -5 | Deteriorating |

---

## Divergence Detection

### The Most Important Breadth Signal

Divergences between headline index price and underlying breadth are among the most reliable early-warning signals for trend reversals. A bearish divergence does not guarantee a reversal, but it significantly increases the probability that the rally is running on fumes.

### Bearish Divergence Detection

**Definition:** Nifty 50 is making new highs or holding near highs, but one or more breadth indicators are deteriorating.

**Detection criteria (any one is sufficient to flag, two or more is a strong signal):**

1. **Price-Breadth Divergence:** Nifty 50 within 2% of its 20-day high, but % of stocks above 200 DMA has declined by more than 5 percentage points over the same 20 days.

2. **A/D Line Divergence:** Nifty 50 making a higher high vs. 20 days ago, but the cumulative A/D Line is making a lower high.

3. **New Highs Divergence:** Nifty 50 at or near all-time/recent highs, but the count of new 52-week highs is lower than the count at the previous Nifty high.

4. **Sector Dropout:** Nifty 50 trending up, but 3 or more sectors have dropped below their 50 DMA in the last 10 trading days.

5. **Cap-Tier Split:** Nifty 50 (large cap) making new highs, but Nifty Smallcap 100 is below its 50 DMA.

### Bullish Divergence Detection

**Definition:** Nifty 50 is making new lows or holding near lows, but breadth indicators are stabilizing or improving.

**Detection criteria:**

1. **Price-Breadth Divergence:** Nifty 50 within 2% of its 20-day low, but % of stocks above 200 DMA has increased by more than 3 percentage points.

2. **A/D Line Divergence:** Nifty 50 making a lower low, but the A/D Line is making a higher low.

3. **New Lows Exhaustion:** Nifty 50 at new lows, but the count of new 52-week lows is lower than at the previous Nifty low (selling exhaustion).

4. **Sector Recovery:** Nifty 50 near lows, but 2 or more sectors have crossed above their 50 DMA in the last 10 days.

### Divergence Severity Scale

| Level | Condition | Duration | Action |
|-------|-----------|----------|--------|
| **Level 1 (Minor)** | 1 indicator diverging | < 1 week | Monitor, no action needed |
| **Level 2 (Moderate)** | 2 indicators diverging | 1-2 weeks | Tighten stops, stop adding new positions |
| **Level 3 (Severe)** | 3+ indicators diverging | 2-3 weeks | Reduce exposure by 20-30% |
| **Level 4 (Extreme)** | All indicators diverging | 3+ weeks | Move to defensive posture (40-60% exposure) |

---

## Using Breadth to Time Equity Allocation

### The Breadth-Based Allocation Framework

Instead of trying to time the market (which is extremely difficult), use breadth to size exposure. Be aggressive when breadth is strong and defensive when it is weak.

### Health Zones and Recommended Exposure

| Score Range | Zone | Target Equity Allocation | Position Sizing | Strategy Bias |
|-------------|------|--------------------------|-----------------|---------------|
| 80-100 | Strong | 90-100% | Full-size positions, add on dips | Momentum, breakout, trend-following |
| 60-79 | Healthy | 75-90% | Normal-size positions | Mix of momentum and value, selective buying |
| 40-59 | Neutral | 60-75% | Reduced positions, quality focus | Defensive quality, sector rotation |
| 20-39 | Weakening | 40-60% | Small positions, large-cap only | Capital preservation, hedging |
| 0-19 | Critical | 25-40% | Minimal positions, cash-heavy | Contrarian for long-term, defensive for short-term |

### Transition Rules

**Increasing exposure (cautious approach):**
- Score must be in the higher zone for 3+ consecutive days before increasing
- Increase gradually: 10% per week, not all at once
- Prioritize stocks and sectors with the strongest individual breadth
- Do not chase — buy on pullbacks within the uptrend

**Decreasing exposure (aggressive approach):**
- Decrease immediately when score drops to a lower zone (do not wait)
- Sell weakest positions first (lowest relative strength)
- Move proceeds to cash, liquid funds, or short-term debt funds
- Consider hedging remaining positions with index puts

**Emergency protocol:**
- If score drops more than 15 points in a single week: reduce exposure by one full zone level immediately
- If A/D ratio goes below 0.5 for 3+ consecutive days: move to Critical zone regardless of composite score
- If Nifty drops more than 5% in a single session: emergency review, consider halving exposure

### The "No-Man's Land" Problem

Scores between 45-55 (mid-Neutral zone) are the hardest to act on. The market could go either way. In this zone:
- Do not make large new commitments
- Maintain existing positions with tight stops
- Wait for the score to decisively move above 60 or below 40 before making significant allocation changes

---

## Historical Case Studies

### Case Study 1: 2020 COVID Crash and Recovery — Breadth as Bottoming Signal

**The Crash (February - March 2020):**
- Feb 20: Nifty at 12,250. Estimated breadth score: ~65 (Healthy). No warnings.
- Mar 12: Nifty at 9,590. Breadth score collapses to ~15 (Critical). Over 85% of stocks below 200 DMA. A/D ratio < 0.3 for multiple sessions.
- Mar 23: Nifty at 7,511 (trough). Breadth score: ~5 (Critical). Virtually every stock below every moving average. New 52-week lows: 400+. New highs: 0.

**The Recovery (April - December 2020):**
- Apr-May: Nifty recovers to 9,500. Breadth score: ~25-30 (Weakening). A/D ratio turns positive (>1.5). New highs reappearing.
- Jun-Jul: Nifty at 10,500-11,000. Breadth score: ~45-50 (Neutral). 40% of stocks above 200 DMA. 7/13 sectors improving.
- Aug-Oct: Nifty at 11,500-12,000. Breadth score: ~60-65 (Healthy). Broad participation returning.
- Nov-Dec: Nifty at 13,000-14,000. Breadth score: ~75 (Healthy/Strong). 65%+ above 200 DMA. All sectors participating.

**Key lesson:** The extreme Critical reading in March 2020 was itself a contrarian signal. When breadth is at absolute extremes (score < 10), the probability of a reversal is high. Traders who began gradually increasing exposure when the breadth score moved from Critical to Weakening (April 2020) captured the strongest part of the recovery.

### Case Study 2: 2021 Broad Bull Market — Breadth Confirmation

**The Rally (January - October 2021):**
- Jan-Mar 2021: Nifty 14,000-15,000. Breadth score: ~70-80 (Healthy to Strong). Midcaps and smallcaps outperforming. 10-11/13 sectors in uptrend.
- Apr-Jun 2021: Brief correction to 14,400 then recovery. Breadth briefly dipped to 55-60 but recovered quickly.
- Jul-Sep 2021: Nifty 15,500-17,500. Breadth score: 80+ (Strong). This was one of the broadest participation markets in NSE history. Over 70% of stocks above 200 DMA.
- Oct 2021: Nifty peaks at 18,600.

**But the divergence:**
- At the Nifty peak of 18,600, midcap and smallcap indices had already peaked in September
- New 52-week highs were declining even as Nifty made new highs
- Only 7/13 sectors participating (down from 11/13 in August)
- Breadth score had dropped from 85+ to ~70 even as Nifty made new highs
- **This was a classic bearish divergence**

**What followed:** Nifty corrected 15% from Oct 2021 to Jun 2022. Midcaps and smallcaps corrected 20-25%.

**Key lesson:** The breadth score correctly confirmed the 2021 bull rally (high scores throughout) and then warned of the top via divergence (falling scores while Nifty made new highs). Traders who reduced exposure when the divergence appeared would have avoided significant losses.

### Case Study 3: 2022 Selective Market — Narrow Breadth Warning

**The Setup (June - December 2022):**
- Nifty recovered from 15,200 (June low) to 18,800 (December)
- This looked like a strong recovery on the index level
- But breadth told a different story:
  - Only 40-50% of stocks above 200 DMA throughout the rally
  - A/D ratio averaging only 1.1-1.3 (marginally positive)
  - Rally concentrated in specific themes: Adani Group stocks, select PSUs, defense sector
  - IT, pharma, and FMCG lagging significantly
  - Estimated breadth score: 40-55 (Neutral) throughout — never reaching Healthy

**Key lesson:** A narrow rally can still take the index higher (Nifty gained 24% from June to December), but the breadth framework correctly identified it as fragile. Traders maintaining 60-75% exposure (per Neutral zone guidance) participated in the upside while limiting risk.

---

## India-Specific Considerations

### F&O Expiry Effects on Breadth

Weekly expiry (Thursday) and monthly expiry (last Thursday of the month) can distort breadth readings:

- **Expiry-day impact:** Delta-hedging by market makers and unwinding of positions can cause artificial price moves in F&O stocks, distorting the A/D ratio.
- **Monthly expiry:** More significant distortion as all stock F&O contracts expire. High open interest stocks can see sharp moves.
- **Recommendation:** Use the 5-day average A/D ratio instead of single-day readings. When analyzing expiry-day breadth, compare to the same day in the previous non-expiry week.

### Budget Day (February 1)

- Extreme single-day breadth swings based on sector-specific announcements
- Infra, defense, agriculture, and housing sectors are most affected
- Budget-day breadth is event-driven, not trend-driven
- **Recommendation:** Do not change regime classification based on budget-day reading alone. Use pre-budget and post-budget (3+ days later) readings for regime assessment.

### RBI Monetary Policy Days

- Typically 6 announcements per year (bi-monthly)
- Rate decisions and stance changes affect banking and NBFC breadth disproportionately
- **Recommendation:** Note the event context. Evaluate banking sector breadth separately on policy days. Wait 2-3 days for the impact to settle before updating the composite score.

### FII/DII Flow Dynamics

- **FII selling pressure:** FIIs are the largest holders of Nifty 50 stocks. Heavy FII selling (Rs 2,000+ Cr/day) initially hits large-cap breadth while mid/small-caps may hold up (supported by DII buying).
- **DII floor:** Monthly SIP flows into mutual funds (Rs 20,000+ Cr/month as of 2024-2025) provide structural support for mid and small caps. This has created a "DII put" that limits breadth deterioration in the broader market.
- **Signal interpretation:** When FII selling is heavy but overall breadth remains resilient, it often precedes a snapback rally once FII selling exhausts. When both FII and DII are selling, expect a broad breadth collapse.

### Monsoon Season (June-September)

- Monsoon performance affects agriculture, rural consumption, FMCG rural sales, and agri-input sectors
- **Good monsoon:** FMCG, fertilizer, tractor/farm equipment, and rural banking stocks participate — adds to breadth
- **Weak/delayed monsoon:** These sectors lag — breadth narrows, especially in the broader Nifty 500
- **Recommendation:** Track monsoon progress (IMD data) and adjust expectations for FMCG/agri sector participation accordingly.

### IPO Market as Leading Indicator

- A vibrant IPO market (many listings, high subscription rates, listing-day gains of 20%+) correlates with broad market risk appetite and healthy breadth
- IPO drought or discount listings correlate with weak breadth and risk-off sentiment
- Surge in SME IPOs with extreme oversubscription (100x+) can signal speculative excess — often a late-stage breadth indicator

### SEBI Regulatory Actions

- SEBI's stress testing directive for small-cap mutual funds (2024) caused episodic breadth disruption in small-cap tier
- Mutual fund categorization rules create structural flows between market cap tiers
- ASM (Additional Surveillance Measure) and GSM (Graded Surveillance Measure) actions on specific stocks can affect new highs/lows counts
- **Recommendation:** Flag regulatory-driven breadth changes separately from organic market-driven changes. These are typically short-lived (1-2 weeks).

### Seasonal and Calendar Patterns

| Period | Effect on Breadth | Notes |
|--------|------------------|-------|
| April (FY start) | Fresh fund allocation, often positive breadth | Mutual funds deploy year-start capital |
| June-Sept (Monsoon) | Mixed, agri-dependent sectors affected | Track IMD monsoon data |
| October (Diwali) | Positive sentiment, Muhurat trading session | Token buying, often positive day |
| January (Budget anticipation) | Sector rotation based on budget expectations | Pre-budget positioning |
| March (FY end) | Tax-loss harvesting, forced selling in small-caps | Distorted breadth readings |
