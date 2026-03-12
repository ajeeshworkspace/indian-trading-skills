# FII/DII Flow Interpretation Guide

## Table of Contents

1. [How to Read FII/DII Data Tables](#how-to-read-fiidii-data-tables)
2. [Bullish Flow Signals](#bullish-flow-signals)
3. [Bearish Flow Signals](#bearish-flow-signals)
4. [Neutral Flow Signals](#neutral-flow-signals)
5. [Combining Flows with Market Breadth and Technical Levels](#combining-flows-with-market-breadth-and-technical-levels)
6. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
7. [FII Derivative Positions as Leading Indicator](#fii-derivative-positions-as-leading-indicator)
8. [Quick Reference Decision Matrix](#quick-reference-decision-matrix)
9. [Practical Examples](#practical-examples)

---

## How to Read FII/DII Data Tables

### Standard Data Format

FII/DII data is typically presented in the following format (all values in Indian Rupees, crores):

| Date | FII Gross Buy | FII Gross Sell | FII Net | DII Gross Buy | DII Gross Sell | DII Net |
|------|-------------|--------------|---------|-------------|--------------|---------|
| 12-Mar-2026 | 8,500 | 10,200 | -1,700 | 7,800 | 6,100 | +1,700 |
| 11-Mar-2026 | 9,200 | 11,800 | -2,600 | 8,500 | 6,300 | +2,200 |
| 10-Mar-2026 | 7,800 | 8,100 | -300 | 6,200 | 6,400 | -200 |

### Understanding the Columns

**Gross Buy:** The total value of shares purchased by FII/DII on that day across all stocks. This number includes all buy transactions regardless of whether the same entity also sold shares.

**Gross Sell:** The total value of shares sold by FII/DII on that day across all stocks.

**Net (Buy-Sell):** Gross Buy minus Gross Sell. This is the most important number:
- **Positive Net = Net buyer**: FII/DII bought more than they sold. Capital is flowing into the market.
- **Negative Net = Net seller**: FII/DII sold more than they bought. Capital is flowing out of the market.
- **Zero or near-zero Net**: Balanced activity, no directional flow.

### Key Reading Principles

1. **Focus on Net, not Gross**: A day with FII Gross Buy of 15,000cr and Gross Sell of 16,000cr (Net = -1,000cr) is mildly bearish. Do not get distracted by the high gross numbers; what matters is the net direction and magnitude.

2. **Look at trends, not individual days**: A single day's data can be noisy. Look at 5-day and 10-day rolling net flows to identify trends.

3. **Compare FII and DII in tandem**: The relationship between FII and DII flows tells a more complete story than either alone.

4. **Note the magnitude**: FII Net of -500cr is noise. FII Net of -5,000cr is a strong signal. Always contextualize the absolute value (refer to significance thresholds in the methodology document).

5. **Check for gross activity level**: If both Gross Buy and Gross Sell are unusually high (say, both above 12,000-15,000cr for FII), it suggests high institutional churning/rotation, even if Net is small. This indicates sector rotation rather than directional flow.

### Monthly and Yearly Aggregation

**MTD (Month-to-Date):** Sum of daily Net values from the 1st of the month to the current date. This shows the monthly trend in progress.

**YTD (Year-to-Date):** Sum of daily Net values from January 1st (or April 1st for FY) to the current date. This shows the annual positioning trend.

**Rolling Averages:**
- 5-day rolling average: Smooths daily noise, shows weekly trend.
- 20-day rolling average: Approximates monthly trend, good for regime identification.

---

## Bullish Flow Signals

The following flow patterns suggest positive market outlook. Listed in order of decreasing signal strength:

### Signal 1: Dual Institutional Buying (Strongest Bullish)

**Pattern:** Both FII and DII are net buyers for 3 or more consecutive trading days.

**What it means:** Foreign and domestic institutions are simultaneously deploying capital. This indicates broad-based institutional confidence. Since FII and DII have different information sets, mandates, and decision frameworks, their alignment is a strong signal.

**How to confirm:**
- Check if combined daily net (FII + DII) exceeds 3,000cr.
- Verify that Nifty is responding with positive closes.
- Check market breadth: advance-decline ratio should be above 1.5:1.
- VIX should be declining or stable.

**Historical success rate:** When both FII and DII buy for 5+ consecutive days, Nifty has historically risen 2-4% in the following 10 trading days approximately 75% of the time.

**Caveats:** This signal is rare (occurs in perhaps 10-15% of trading periods). When it does occur, much of the move may already be priced in by the time the data is published.

### Signal 2: FII Turning Net Buyer After Sustained Selling

**Pattern:** FII have been net sellers for 10+ trading days (or a full month) and then post 3+ consecutive days of net buying.

**What it means:** The selling pressure that was weighing on markets has exhausted. FII have either completed their de-risking or are re-entering based on improved valuations/outlook. This is often the start of a new uptrend.

**How to confirm:**
- FII net buying days should show increasing magnitude (Day 1: +500cr, Day 2: +1,200cr, Day 3: +2,000cr).
- Nifty should be breaking above the range it was stuck in during the selling phase.
- USD/INR should be stabilizing or declining.
- FII derivative data should show long buildup in index futures.

**Historical success rate:** FII regime transitions from seller to buyer have preceded Nifty rallies of 3-8% over the following month approximately 70% of the time.

**Caveats:** False starts happen. FII may buy for 2-3 days and then resume selling. Always wait for confirmation (5+ days of buying or MTD turning positive) before considering this a regime change.

### Signal 3: DII Buying Accelerating During FII Selling

**Pattern:** FII are selling, but DII buying is not only absorbing FII outflow but exceeding it, resulting in net positive institutional flow.

**What it means:** Domestic institutions see value at current levels that FII are missing. DII buying exceeding FII selling suggests the market has strong domestic demand support and the selling is being treated as a buying opportunity by domestic money managers.

**How to confirm:**
- Calculate absorption rate: (DII Net / abs(FII Net)) > 100%.
- Nifty should be holding support levels or forming a base.
- SIP flow data should be stable or growing.
- Check if MF cash levels are declining (indicating deployment).

### Signal 4: FII Net Buying with Rising Gross Activity

**Pattern:** FII Net is positive, and Gross Buy is significantly higher than the 20-day average.

**What it means:** FII are not just passively buying; they are actively increasing their India allocation. High gross buy with positive net indicates conviction buying, not just short-covering or routine rebalancing.

**How to confirm:**
- FII Gross Buy should be 20-30% above the 20-day average.
- The buying should be accompanied by positive Nifty movement.
- Look for large-cap financial stocks (Bank Nifty) outperforming, as this typically indicates FII large-cap buying.

### Signal 5: FII Selling Decelerating

**Pattern:** FII remain net sellers, but the daily net selling amount is declining over 5+ days (e.g., -4,000cr, -3,000cr, -2,000cr, -1,500cr, -800cr).

**What it means:** The worst of FII selling may be over. While still negative, the declining intensity suggests exhaustion of the selling driver. This is often a precursor to Signal 2 (FII turning net buyer).

**How to confirm:**
- Plot the 5-day trend line of FII net. Slope should be turning upward (becoming less negative).
- Nifty should be stabilizing (daily declines getting smaller).
- Check the fundamental driver of selling: if the catalyst is fading (e.g., US yields stabilizing after Fed meeting), the deceleration is likely genuine.

---

## Bearish Flow Signals

The following flow patterns suggest caution or negative market outlook:

### Signal 1: Sustained FII Selling Above Significance Threshold (Strongest Bearish)

**Pattern:** FII net selling exceeds 2,000cr per day for 5+ consecutive trading days, with weekly cumulative exceeding 10,000-15,000cr.

**What it means:** FII are engaged in systematic de-risking of India exposure. This is not profit-booking or portfolio rebalancing; this is a directional call against the Indian market. Sustained selling of this magnitude typically reflects a macro-level decision (global risk-off, India downgrade, policy concern).

**How to confirm:**
- FII selling should be consistent (no days of net buying breaking the streak).
- DII should be unable to fully absorb (absorption rate < 80%).
- Nifty should be making lower lows and lower highs.
- USD/INR should be rising (INR weakening).
- India VIX should be elevated (above 16-18).

**Market impact:** When this pattern persists for 2+ weeks, Nifty typically declines 5-10% from the start of the selling phase.

**Historical examples:** October 2021 to June 2022 (prolonged FII selling), October 2024 (extreme monthly selling).

### Signal 2: DII Unable to Absorb FII Selling

**Pattern:** FII are net sellers, and DII are net buyers, but DII absorption rate is below 60% for 5+ days.

**What it means:** The selling pressure is overwhelming domestic demand. Even with strong SIP flows, the magnitude of FII selling is too large for DII to offset. This creates a net negative institutional flow, putting pressure on prices.

**How to confirm:**
- Calculate daily absorption rate: DII Net / abs(FII Net).
- If consistently below 60%, the market lacks sufficient buy-side support.
- Nifty should be declining or failing to bounce from support levels.
- Check if DII buying is actually declining (possible if MFs face redemptions in a falling market, creating a negative feedback loop).

### Signal 3: Dual Institutional Selling (Strongest Bearish, Rare)

**Pattern:** Both FII and DII are net sellers for 2+ consecutive days.

**What it means:** This is the most dangerous flow signal. When both foreign and domestic institutions are selling simultaneously, it indicates a systemic concern. There is no institutional buying support for the market.

**How to confirm:**
- Both FII and DII Net should be negative for 2+ days.
- Combined daily outflow should exceed 2,000cr.
- Market breadth should be very poor (advance-decline below 0.3:1).
- VIX should be spiking.

**Historical context:** Dual selling is extremely rare (occurred briefly during COVID March 2020, during the demonetization shock in November 2016, and during isolated panic days). It typically does not last more than 3-5 days because DII SIP flows automatically create buying.

**Action implication:** If this signal appears, extreme caution is warranted. It often coincides with 3-5% single-day or multi-day market crashes.

### Signal 4: FII Selling Accelerating

**Pattern:** FII daily net selling is increasing in magnitude over 5+ days (e.g., -1,500cr, -2,200cr, -3,000cr, -4,500cr, -5,800cr).

**What it means:** The selling is not a one-time adjustment; it is intensifying. Each day, more capital is leaving. This suggests the underlying driver is worsening (e.g., escalating geopolitical crisis, accelerating rate hikes, deteriorating India macro).

**How to confirm:**
- Plot the 5-day trend of FII net. Slope should be steepening downward.
- Look for the catalyst: news flow should reveal the fundamental driver.
- Check global EM flow data: if selling is India-specific, it is more bearish than if it is a broad EM phenomenon.

### Signal 5: FII Buying Exhausting After Brief Return

**Pattern:** After a period of selling, FII bought for 2-3 days, then reverted to selling.

**What it means:** The initial buying was likely short-covering, month-end rebalancing, or a reactive bounce, not a genuine change in positioning. The quick reversion suggests the structural selling driver is intact.

**How to confirm:**
- The 2-3 buying days should have had declining magnitude.
- Nifty should have failed to sustain the bounce.
- FII derivative data should still show net short or declining long positions.

---

## Neutral Flow Signals

### Signal 1: Mixed Flows with Low Absolute Values

**Pattern:** FII and DII alternate between small net buying and selling days. Absolute daily net values are below 1,000cr for both.

**What it means:** Neither FII nor DII have a strong directional view. Institutional money is in wait-and-watch mode. This typically occurs:
- Between major events (between Fed meetings, between earnings seasons)
- When valuations are fair (not cheap enough to buy aggressively, not expensive enough to sell)
- During holiday-impacted low-volume weeks

**Market implication:** Nifty is likely range-bound. Direction will be driven by stock-specific factors, news flow, or retail activity.

### Signal 2: FII and DII Flows Offsetting Exactly

**Pattern:** FII net selling approximately equals DII net buying (or vice versa) consistently. Combined net is near zero.

**What it means:** A liquidity equilibrium. Foreign money leaving is being precisely replaced by domestic money. The market finds a price level where both sides are comfortable.

**Market implication:** Nifty consolidates in a range. Breakout will occur when one side changes behavior (FII stops selling, or DII buying slows).

### Signal 3: High Gross Activity but Low Net

**Pattern:** FII Gross Buy and Gross Sell are both very high (say, 12,000-15,000cr each), but Net is close to zero.

**What it means:** Heavy institutional churning and sector rotation. FII are actively buying some stocks/sectors while selling others. The overall allocation to India is not changing, but the composition is shifting.

**Market implication:** Index may be stable, but significant sector/stock-level moves. Look for which sectors are seeing FII buying (will outperform) and which are seeing selling (will underperform).

---

## Combining Flows with Market Breadth and Technical Levels

Flow data becomes much more powerful when combined with other market indicators:

### Flow + Market Breadth

| FII Flow | Market Breadth (A/D) | Interpretation |
|----------|---------------------|----------------|
| FII buying | Breadth > 2:1 | Strong broad-based rally, sustainable |
| FII buying | Breadth < 1:1 | Index-driven rally (FII buying index heavyweights), narrow, fragile |
| FII selling | Breadth > 1.5:1 | Market resilient despite FII selling (DII/retail buying breadth stocks) |
| FII selling | Breadth < 0.5:1 | Broad-based decline, high risk |

### Flow + Nifty Technical Levels

**FII buying at Nifty support levels:** Very bullish. Smart money is buying at technically significant levels, likely to trigger a bounce.

**FII selling at Nifty resistance levels:** Bearish. FII are selling into strength, which suggests the resistance level will hold and Nifty may pull back.

**FII buying as Nifty breaks above resistance:** Momentum signal. FII buying into a breakout suggests the move is likely to sustain.

**FII selling as Nifty breaks below support:** Capitulation signal. FII selling into a breakdown amplifies the move and suggests lower levels.

### Flow + VIX (India VIX)

| FII Flow | VIX Level | Interpretation |
|----------|-----------|----------------|
| FII buying | VIX < 13 | Complacent buying; late-stage rally |
| FII buying | VIX 13-18 | Healthy buying; sustainable trend |
| FII selling | VIX 18-25 | Elevated fear, but not panic; watch for DII absorption |
| FII selling | VIX > 25 | Panic selling; potential capitulation and reversal zone |

### Flow + Nifty PE Valuation

| FII Flow | Nifty Trailing PE | Interpretation |
|----------|--------------------|----------------|
| FII buying | PE < 18 | Value buying; strong fundamental support |
| FII buying | PE 18-22 | Fair-value buying; earnings-driven |
| FII buying | PE > 22 | Momentum/FOMO buying; elevated risk |
| FII selling | PE > 22 | Valuation-driven selling; rational de-risking |
| FII selling | PE < 18 | Forced selling (panic/redemptions); potential bottom |

---

## Common Mistakes to Avoid

### Mistake 1: Over-Reacting to Single-Day Data

**The error:** Seeing "FII sold 4,000cr today" and concluding the market will crash.

**Why it is wrong:** Single-day data is noisy. A large daily sell number can be caused by:
- A single block deal (PE fund selling stake)
- Derivative expiry-related hedging adjustments
- Quarterly rebalancing by a large FPI
- IPO/OFS settlement flows

**Correct approach:** Always look at the 5-day and 10-day rolling sum. A single day of -4,000cr followed by +2,000cr and +1,500cr the next two days is a net -500cr over 3 days, which is noise. The trend matters, not the individual data point.

### Mistake 2: Ignoring Derivative Market Flows

**The error:** Forming a view solely based on cash market FII/DII data.

**Why it is wrong:** FII derivative positions are often a leading indicator. FII may be net buyers in cash but building short positions in index futures (hedging their portfolio). The cash buying looks bullish, but the net exposure (cash + derivatives) may be neutral or bearish.

**Correct approach:** Always check FII derivative data (available from NSE Participant-wise OI data) alongside cash flow data. Key metric: FII net long/short contracts in index futures.

### Mistake 3: Treating All FII as One Entity

**The error:** Assuming "FII are selling" means all foreign investors share the same bearish view.

**Why it is wrong:** FII/FPI includes thousands of entities with different strategies, mandates, and time horizons. Global pension funds have different views than EM hedge funds. Passive ETFs rebalance mechanically while active funds make discretionary calls. Aggregate data masks significant heterogeneity.

**Correct approach:** When possible, differentiate between categories:
- Are passive funds selling (MSCI rebalancing)? This is temporary and mechanical.
- Are active EM funds selling? This may reflect a genuine bearish view.
- Is selling concentrated in one category? Check NSDL FPI category-wise data for monthly breakdowns.

### Mistake 4: Linear Extrapolation of Trends

**The error:** FII sold 20,000cr this week, so they will sell 20,000cr next week too, and the market will fall further.

**Why it is wrong:** FII flows can reverse rapidly. The driver of selling may resolve (Fed becomes dovish, geopolitical tension eases), or prices may fall enough to make India attractive again. Flow trends are mean-reverting, not permanent.

**Correct approach:** Instead of extrapolating, identify the catalyst for the current flow pattern and assess whether it is strengthening or weakening. If the catalyst is fading, expect flows to moderate or reverse.

### Mistake 5: Confusing Correlation with Causation

**The error:** FII bought, and Nifty rose, therefore FII buying caused the rally.

**Why it is wrong:** Both FII buying and Nifty rising may be caused by a third factor (positive earnings, rate cut, global risk-on). FII buying is also partly reactive: when markets rise, FII may buy more to increase allocation to a performing market.

**Correct approach:** Use FII flow data as one input among many. Combine with fundamental analysis, technical analysis, macro data, and sentiment indicators to form a holistic view.

### Mistake 6: Ignoring the Calendar

**The error:** Treating FII selling on MSCI rebalancing day or F&O expiry week the same as regular selling.

**Why it is wrong:** Certain calendar events create mechanical flows that do not reflect genuine positioning changes:
- MSCI/FTSE quarterly rebalancing (February, May, August, November) triggers passive FII flows.
- F&O monthly expiry (last Thursday) creates hedging-related cash market flows.
- Quarterly earnings season triggers stock-specific institutional activity.
- March (FY end) triggers tax-related and rebalancing flows.

**Correct approach:** Flag these calendar events and interpret flow data accordingly. Flows during these periods may be larger in absolute terms but less meaningful directionally.

### Mistake 7: Not Adjusting for Market Cap Growth

**The error:** Comparing FII selling of 10,000cr/month in 2015 with the same figure in 2025 as equally significant.

**Why it is wrong:** Indian market capitalization has roughly quadrupled from approximately 100 lakh crore in 2015 to approximately 400 lakh crore in 2025. The same absolute flow represents a much smaller percentage of the market.

**Correct approach:** Express flows as a percentage of market cap, or at minimum, adjust significance thresholds over time. A flow of 10,000cr/month was 0.1% of market cap in 2015 but only 0.025% in 2025.

---

## FII Derivative Positions as Leading Indicator

### Why Derivative Data Matters

FII derivative positions in Indian markets provide a critical leading signal for cash market flows:

1. **Derivatives allow leverage**: FII can express large directional views through futures with only margin capital. Changes in derivative positions amplify the signal from cash market data.

2. **Derivatives precede cash**: FII typically establish derivative positions before deploying or withdrawing cash. A buildup of FII long positions in index futures often precedes cash market buying by 1-5 trading days.

3. **Put-Call Ratio (PCR)**: FII activity in index options (Nifty/Bank Nifty puts and calls) provides sentiment information. High FII put buying suggests hedging/bearishness; high FII call buying suggests bullishness.

### Key Derivative Metrics to Track

**FII Index Futures Net OI (Open Interest):**
- This is the single most important derivative metric.
- Net long (more long contracts than short contracts) = FII bullish on market direction.
- Net short (more short contracts than long contracts) = FII bearish on market direction.
- The absolute number of contracts and the daily change both matter.

**FII Index Futures Long/Short Ratio:**
- Ratio = Long contracts / Short contracts.
- Above 1.0 = net long (bullish). Above 2.0 = strongly bullish.
- Below 1.0 = net short (bearish). Below 0.5 = strongly bearish.
- Historical average is approximately 0.6-0.8 (FII tend to maintain a slight net short as hedging for their long cash positions).

**FII Stock Futures Net OI:**
- FII net long in stock futures indicates bullish positioning on specific stocks.
- FII net short in stock futures indicates bearish single-stock views or hedging.
- Stock futures are less reliable as a directional indicator than index futures because they include hedging positions.

**FII Index Options Activity:**
- FII call buying: Bullish or upside hedging.
- FII put buying: Bearish or downside hedging.
- FII put writing: Bullish (selling insurance = confident market won't fall).
- FII call writing: Bearish (selling upside = confident market won't rally).

### Interpreting Derivative Data Alongside Cash Flows

| Cash Flow | Derivative Position | Combined Interpretation |
|-----------|-------------------|----------------------|
| FII cash buying | FII index futures net long increasing | Strongly bullish. Cash + derivative alignment. |
| FII cash buying | FII index futures net short increasing | Cautious. Buying cash but hedging via futures. Net exposure may be neutral. |
| FII cash selling | FII index futures net short increasing | Strongly bearish. Selling cash + adding derivative shorts. |
| FII cash selling | FII index futures net long increasing | Complex. May be selling expensive large-caps and buying index futures (relative value trade). Less bearish than it appears. |
| FII cash neutral | FII index futures net long increasing | Moderately bullish. Positioning via derivatives before cash deployment. Watch for cash buying to follow. |
| FII cash neutral | FII index futures net short increasing | Moderately bearish. Hedging or building bearish positions without selling cash (may be locked in due to disclosure thresholds). |

### Where to Find FII Derivative Data

- **NSE Daily Reports**: "Participant-wise Trading in Equity Derivatives" published daily after market hours.
- **NSE FII Derivative Statistics**: Aggregate FII long/short contracts in index futures, stock futures, index options, and stock options.
- **MoneyControl/Trendlyne**: Aggregated FII derivative data with historical charts.

---

## Quick Reference Decision Matrix

Use this matrix for rapid assessment of the institutional flow environment:

| # | FII Cash | DII Cash | FII Derivatives | Market Regime | Nifty Outlook | Confidence |
|---|----------|----------|-----------------|---------------|---------------|------------|
| 1 | Strong buy (>2000cr/day) | Buy | Net long increasing | Dual buying | Bullish | High |
| 2 | Strong buy | Sell | Net long increasing | FII-driven rally | Bullish (narrow) | Medium |
| 3 | Strong sell (<-2000cr/day) | Strong buy (absorbing >80%) | Net short | DII absorption | Range-bound | Medium |
| 4 | Strong sell | Buy (absorbing <60%) | Net short increasing | Bearish pressure | Bearish | High |
| 5 | Strong sell | Sell | Net short increasing | Dual selling (rare) | Strongly bearish | Very High |
| 6 | Mild sell (-500 to -2000cr) | Mild buy | Neutral | Mild headwind | Slightly negative | Low |
| 7 | Neutral (<500cr either way) | Neutral | Neutral | No signal | Directionless | Very Low |
| 8 | Turning from sell to buy | Buy | Long building | Transition to bullish | Positive bias | Medium |
| 9 | Turning from buy to sell | Sell | Short building | Transition to bearish | Negative bias | Medium |

---

## Practical Examples

### Example 1: Reading a Bullish Flow Setup

**Data observed:**

| Date | FII Net | DII Net | Nifty Close | Nifty Change |
|------|---------|---------|-------------|-------------|
| Day 1 | +1,200 | +800 | 22,400 | +0.6% |
| Day 2 | +2,300 | +1,100 | 22,650 | +1.1% |
| Day 3 | +1,800 | +600 | 22,730 | +0.4% |
| Day 4 | +3,100 | +400 | 22,900 | +0.7% |
| Day 5 | +2,500 | +900 | 23,050 | +0.7% |

**Interpretation:**
- FII have been net buyers for 5 consecutive days (cumulative: +10,900cr). This crosses the significance threshold for a weekly sum.
- DII are also net buyers, though with smaller amounts (cumulative: +3,800cr). Dual buying regime.
- FII buying magnitude is increasing (1,200 to 3,100), suggesting accelerating conviction.
- Nifty has responded positively each day, confirming flow-price alignment.
- Combined 5-day inflow: +14,700cr. This is very strong.

**Assessment:** This is a Signal 1 (Dual Institutional Buying) bullish pattern. The trend is strong and accelerating. Expect continued upside unless a major external catalyst disrupts.

**What to watch:** FII derivative data should confirm this (net long increasing). If FII are buying cash but their derivative longs are not increasing, the buying may be short-term (MSCI rebalancing, month-end flows).

### Example 2: Reading a Bearish Flow Setup

**Data observed:**

| Date | FII Net | DII Net | Nifty Close | Nifty Change |
|------|---------|---------|-------------|-------------|
| Day 1 | -2,800 | +1,500 | 23,800 | -0.8% |
| Day 2 | -3,500 | +2,200 | 23,550 | -1.0% |
| Day 3 | -4,200 | +2,800 | 23,300 | -1.1% |
| Day 4 | -5,100 | +3,100 | 22,950 | -1.5% |
| Day 5 | -4,800 | +2,600 | 22,700 | -1.1% |

**Interpretation:**
- FII selling is heavy and accelerating (2,800 to 5,100), crossing the extreme threshold.
- DII buying is increasing in response (counter-cyclical behavior from SIPs and value-buying).
- Absorption rate: Day 1: 54%, Day 2: 63%, Day 3: 67%, Day 4: 61%, Day 5: 54%. DII are absorbing only 54-67%, insufficient to prevent decline.
- Nifty is making lower lows each day, with selling pressure increasing.
- Cumulative 5-day FII outflow: -20,400cr. Cumulative DII inflow: +12,200cr. Net institutional outflow: -8,200cr.

**Assessment:** This is a Signal 1 (Sustained FII Selling) + Signal 2 (DII Unable to Absorb) bearish pattern. The trend is strongly negative and intensifying. Nifty likely to see further 3-5% downside unless FII selling decelerates.

**What to watch:** Track the catalyst (likely global, such as US rate hike or geopolitical event). If the catalyst shows signs of resolution, FII selling may peak. Look for a day where FII selling drops below 2,000cr as a potential deceleration signal. Also monitor DII: if DII buying starts to decline (SIP flow slowing, MF redemptions increasing), the downside risk multiplies.

### Example 3: Reading a Transition Setup

**Data observed:**

| Date | FII Net | DII Net | Nifty Close | Nifty Change |
|------|---------|---------|-------------|-------------|
| Day 1 | -3,200 | +2,800 | 21,800 | -0.9% |
| Day 2 | -2,100 | +1,900 | 21,700 | -0.5% |
| Day 3 | -800 | +600 | 21,750 | +0.2% |
| Day 4 | +400 | +300 | 21,850 | +0.5% |
| Day 5 | +1,200 | +500 | 22,000 | +0.7% |

**Interpretation:**
- FII selling decelerated from -3,200 to -800, then turned to net buying (+400, +1,200).
- This is a textbook transition from seller to buyer regime.
- DII buying also decreased in tandem (less need to absorb as FII selling reduced).
- Nifty has found a base around 21,700 and is beginning to recover.
- The transition took 5 days, with Day 3 being the pivot day (FII selling below noise threshold).

**Assessment:** This is a Signal 2 (FII Turning Net Buyer After Sustained Selling) bullish transition. If FII buying continues for 2-3 more days, this confirms a regime change.

**What to watch:** Day 6 and Day 7 are critical. If FII net remains positive and above +1,000cr, the regime change is confirmed. If FII revert to selling on Day 6, it was a false start (Signal 5 bearish). Also check FII derivative positions: if index futures longs are increasing, the transition is genuine.

### Example 4: Reading a Churning/Rotation Setup

**Data observed:**

| Date | FII Gross Buy | FII Gross Sell | FII Net | DII Net | Nifty Change |
|------|-------------|--------------|---------|---------|-------------|
| Day 1 | 14,500 | 14,200 | +300 | -100 | +0.1% |
| Day 2 | 15,200 | 15,800 | -600 | +400 | -0.2% |
| Day 3 | 13,800 | 13,500 | +300 | +200 | +0.3% |
| Day 4 | 16,100 | 15,900 | +200 | -300 | -0.1% |
| Day 5 | 14,900 | 14,600 | +300 | +100 | +0.2% |

**Interpretation:**
- FII Net is minimal (between -600 and +300). Noise-level directional flow.
- However, FII Gross Buy and Gross Sell are both very high (13,500-16,100cr range). Normal gross activity for FII is approximately 8,000-12,000cr.
- This elevated gross activity with low net means heavy sector/stock rotation. FII are actively reallocating within their India portfolio.
- DII flows are also minimal and mixed.
- Nifty is essentially flat.

**Assessment:** This is a Signal 3 (High Gross Activity, Low Net) neutral pattern. No directional signal for Nifty. The important action is happening at the sector/stock level.

**What to investigate:** Use stock-level data (if available) or sector index performance to identify where FII are rotating. For example, if Bank Nifty is outperforming while IT index is underperforming, FII may be rotating from IT to Financials.
