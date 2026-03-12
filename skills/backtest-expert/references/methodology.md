# Backtesting Methodology Reference — Indian Markets (NSE/BSE)

## Table of Contents

1. [Stress Testing Methods](#stress-testing-methods)
2. [Parameter Sensitivity Analysis](#parameter-sensitivity-analysis)
3. [Slippage Modeling for NSE](#slippage-modeling-for-nse)
4. [Commission Structure](#commission-structure)
5. [Sample Size Guidelines](#sample-size-guidelines)
6. [Market Regime Definitions](#market-regime-definitions)
7. [Common Biases](#common-biases)
8. [Walk-Forward Analysis](#walk-forward-analysis)
9. [Statistical Validation](#statistical-validation)

---

## Stress Testing Methods

Stress testing is the most important phase of backtesting. A strategy that survives stress testing across multiple dimensions is far more likely to perform in live trading.

### 1. Parameter Perturbation (Heat Map Analysis)

**Goal:** Verify that the strategy works across a range of parameter values, not just one optimized set.

**Method:**
1. Identify all free parameters (e.g., EMA length, RSI threshold, stop loss %)
2. Create a grid of values: base +/- 10%, +/- 20%, +/- 50%
3. Run the backtest for every combination
4. Plot a heat map of returns (or Sharpe ratio) across the parameter space

**Interpreting heat maps:**

```
GOOD: Broad plateau of profitability      BAD: Sharp peak at one value
+------+------+------+------+             +------+------+------+------+
| 1.2  | 1.4  | 1.5  | 1.3  |            | -0.2 | 0.1  | 2.8  | -0.1 |
+------+------+------+------+             +------+------+------+------+
| 1.3  | 1.5  | 1.6  | 1.4  |            | -0.3 | 0.2  | 0.4  | -0.2 |
+------+------+------+------+             +------+------+------+------+
| 1.1  | 1.3  | 1.4  | 1.2  |            | -0.5 | -0.1 | 0.1  | -0.4 |
+------+------+------+------+             +------+------+------+------+
  Robust strategy                           Overfit strategy
```

**Indian market consideration:** Include market-hours parameters. Some strategies use different parameters for the opening auction (9:15-9:30), mid-day, and closing hour (2:30-3:30). Test sensitivity to these time windows.

### 2. Monte Carlo Simulation

**Goal:** Understand the distribution of possible outcomes, not just the single backtest path.

**Method:**
1. Take the trade-by-trade results from the backtest
2. Randomly reshuffle the order of trades (10,000+ iterations)
3. For each shuffle, calculate drawdown, CAGR, and Sharpe
4. Plot the distribution of outcomes

**What to look for:**
- 5th percentile drawdown (your "realistic worst case")
- Median vs mean CAGR (if very different, a few trades drive returns)
- Probability of a 12-month loss (should be <20% for deployment)

### 3. Regime-Based Testing

**Goal:** Verify the strategy works (or at least does not blow up) across different market environments.

**Method:**
1. Tag each period with its market regime (see regime definitions below)
2. Run the backtest separately for each regime
3. The strategy must be profitable in at least 3 of 5 major regimes
4. Acceptable: flat or small loss in adverse regimes
5. Unacceptable: catastrophic drawdown in any single regime

### 4. Synthetic Stress Events

**Goal:** Test against extreme scenarios that may not appear in historical data.

**Scenarios for Indian markets:**
- Flash crash: Nifty drops 10% intraday (happened in 2012, 2015)
- Circuit limit lock: Stock hits lower circuit for 3+ consecutive days
- Sudden gap: Stock gaps down 15% on earnings miss
- Liquidity freeze: Bid-ask spread widens 5x during panic
- Exchange outage: NSE systems go down for 3+ hours (happened in 2021)
- F&O ban: Stock enters ban period, cannot add positions
- Global contagion: Foreign fund selling exceeding Rs 5,000 Cr/day for 10+ days

### 5. Walk-Forward Stress

**Goal:** Confirm the strategy generalizes to unseen data.

**Method:**
1. Divide data into K folds (e.g., 5 x 2-year periods)
2. Train on K-1 folds, test on the remaining fold
3. Rotate and repeat
4. The combined out-of-sample results are the true performance estimate

---

## Parameter Sensitivity Analysis

### What Counts as a Parameter?

| Counts as Parameter | Does NOT Count |
|---------------------|----------------|
| Moving average length (20 in EMA-20) | Choice of exchange (NSE vs BSE) |
| RSI overbought/oversold thresholds | Time of day to trade (if based on market hours) |
| Stop loss percentage | Universe definition (if rule-based, e.g., "Nifty 200") |
| Profit target percentage | Direction (long-only, short-only) |
| Lookback period for any indicator | Position sizing formula (if mathematically derived) |
| Volume multiplier threshold | |
| ATR multiplier for stops | |

### Parameter Count Guidelines

| Parameters | Risk Level | Notes |
|------------|-----------|-------|
| 1-2 | Low | Simple, robust strategies. Hard to overfit. |
| 3-4 | Moderate | Acceptable if each parameter has a logical reason. |
| 5-6 | High | Must show very strong out-of-sample performance. |
| 7+ | Very High | Almost certainly overfit. Reduce before proceeding. |

### Degrees of Freedom Rule

**Rule of thumb:** You need at least 10-20 trades per free parameter for statistical validity.

| Parameters | Minimum Trades | Recommended Trades |
|------------|---------------|-------------------|
| 2 | 40 | 100+ |
| 3 | 60 | 150+ |
| 4 | 80 | 200+ |
| 5 | 100 | 250+ |

### Running Sensitivity Analysis

For each parameter, create a table:

```
Parameter: EMA Length
Base value: 20
Tested range: 10 to 40, step 2

| Value | CAGR | Sharpe | Max DD | Win Rate | Trades |
|-------|------|--------|--------|----------|--------|
| 10    | 12%  | 0.8    | 22%    | 54%      | 310    |
| 12    | 14%  | 0.9    | 20%    | 55%      | 285    |
| 14    | 15%  | 1.0    | 18%    | 57%      | 260    |
| ...   | ...  | ...    | ...    | ...      | ...    |
| 20    | 16%  | 1.1    | 17%    | 58%      | 220    |  <-- Base
| ...   | ...  | ...    | ...    | ...      | ...    |
| 40    | 10%  | 0.7    | 25%    | 52%      | 150    |

Verdict: STABLE — CAGR remains positive across full range.
         Sharpe degrades gracefully. Acceptable for deployment.
```

---

## Slippage Modeling for NSE

### What is Slippage?

Slippage is the difference between the price you see on the screen and the price you actually get filled at. It includes:
1. Bid-ask spread cost
2. Market impact (your order moving the price)
3. Latency (price moves between decision and execution)

### Typical Slippage by Category (NSE)

| Category | Typical Bid-Ask Spread | Slippage Per Side | Round-Trip |
|----------|----------------------|-------------------|------------|
| Nifty 50 stocks | 0.02-0.05% | 0.03-0.05% | 0.06-0.10% |
| Nifty Next 50 | 0.05-0.10% | 0.05-0.08% | 0.10-0.16% |
| Midcap 150 | 0.10-0.20% | 0.08-0.15% | 0.16-0.30% |
| Smallcap 250 | 0.20-0.50% | 0.15-0.30% | 0.30-0.60% |
| Micro/Nano cap | 0.50-2.00% | 0.30-1.00% | 0.60-2.00% |
| Nifty options (ATM, near expiry) | 0.5-1.0 pts | Rs 2-5 per lot | Varies |
| Nifty options (OTM, far expiry) | 2-5 pts | Rs 5-15 per lot | Varies |
| Bank Nifty options (ATM) | 1-3 pts | Rs 5-10 per lot | Varies |
| Stock options (liquid) | 1-5% of premium | Significant | Varies |
| Stock futures (liquid) | 0.03-0.08% | 0.05-0.10% | 0.10-0.20% |

### Slippage Factors

1. **Time of day:**
   - 9:15-9:30 AM: Highest slippage (opening volatility, wider spreads)
   - 9:30-2:30 PM: Normal slippage
   - 2:30-3:15 PM: Moderate (expiry-day squeezes in F&O)
   - 3:15-3:30 PM: Can spike on closing-order imbalances

2. **Order size relative to liquidity:**
   - Order < 1% of daily volume: Minimal impact
   - Order 1-5% of daily volume: Moderate impact (add 0.05-0.10%)
   - Order > 5% of daily volume: Significant impact (add 0.10-0.30%)

3. **Volatility regime:**
   - India VIX < 15: Normal spreads
   - India VIX 15-25: Spreads widen 1.5-2x
   - India VIX > 25: Spreads widen 2-5x

4. **Event days:**
   - Budget day: Spreads 3-5x normal
   - RBI policy day: Spreads 2-3x for banking stocks
   - Election results: Spreads 5-10x, circuit limits possible
   - Monthly F&O expiry: Options spreads widen significantly in last hour

### How to Model Slippage in Backtests

**Conservative approach (recommended):**
```
For Nifty 50 stocks:     Add 0.05% per side (0.10% round-trip)
For Nifty 100 stocks:    Add 0.08% per side (0.16% round-trip)
For Midcap stocks:       Add 0.15% per side (0.30% round-trip)
For Smallcap stocks:     Add 0.25% per side (0.50% round-trip)
For Index options (ATM): Add Rs 2-3 per lot per side
For Stock options:       Add 2-3% of premium per side
```

**Aggressive test (break test):**
Double all the above values. If the strategy is still profitable, it is robust to execution friction.

---

## Commission Structure

### Discount Broker (Zerodha, Groww, etc.) — 2024/2025 Rates

| Component | Delivery (CNC) | Intraday (MIS) | F&O Futures | F&O Options |
|-----------|----------------|-----------------|-------------|-------------|
| **Brokerage** | Rs 0 or Rs 20/order | Rs 20/order or 0.03% | Rs 20/order or 0.03% | Rs 20/order flat |
| **STT** | 0.1% (buy+sell) | 0.025% (sell only) | 0.0125% (sell) | 0.0625% on premium (sell) |
| **Exchange charges** | 0.00345% (NSE) | 0.00345% (NSE) | 0.002% | 0.05% |
| **GST** | 18% on (brokerage + exchange) | 18% | 18% | 18% |
| **Stamp duty** | 0.015% (buy) | 0.003% (buy) | 0.002% (buy) | 0.003% (buy) |
| **SEBI charges** | 0.0001% | 0.0001% | 0.0001% | 0.0001% |
| **DP charges** | Rs 15.93/scrip (sell) | N/A | N/A | N/A |

### Full Service Broker (ICICI Direct, HDFC Securities, etc.)

| Component | Typical Rate |
|-----------|-------------|
| Brokerage | 0.25-0.50% or Rs 25-35/order |
| Other charges | Same as above |

### Total Cost Examples (Round-Trip)

| Scenario | Trade Value | Total Cost | Cost % |
|----------|-----------|------------|--------|
| Delivery, Rs 50,000, discount broker | Rs 50,000 | ~Rs 155 | ~0.31% |
| Delivery, Rs 2,00,000, discount broker | Rs 2,00,000 | ~Rs 500 | ~0.25% |
| Intraday, Rs 50,000, discount broker | Rs 50,000 | ~Rs 65 | ~0.13% |
| Nifty Futures, 1 lot (~Rs 12,00,000) | Rs 12,00,000 | ~Rs 115 | ~0.01% |
| Nifty Option, 1 lot, premium Rs 200 | Rs 15,000 | ~Rs 55 | ~0.37% |
| Bank Nifty Option, 1 lot, premium Rs 300 | Rs 4,500 | ~Rs 55 | ~1.22% |

### Key Takeaway for Backtesting

- **Delivery trades:** Model 0.25-0.40% round-trip cost
- **Intraday trades:** Model 0.10-0.20% round-trip cost
- **F&O futures:** Model 0.02-0.05% round-trip cost
- **F&O options:** Model 0.50-1.50% of premium as round-trip cost (highly variable)

**Always add slippage on top of commissions.**

---

## Sample Size Guidelines

### Minimum Trade Counts

| Confidence Level | Minimum Trades | Notes |
|-----------------|---------------|-------|
| **Anecdotal** | < 30 | Cannot draw any statistical conclusions |
| **Directional** | 30-50 | Can identify if the strategy has a positive or negative edge |
| **Moderate** | 50-100 | Confidence intervals are still wide (+/- 30-40%) |
| **Good** | 100-200 | Reasonable confidence, can estimate parameters |
| **Strong** | 200-500 | Narrow confidence intervals, reliable statistics |
| **Very Strong** | 500+ | High confidence, can detect small edges |

### Statistical Tests for Trade Significance

**1. t-test for mean trade return:**
```
H0: Mean trade return = 0 (no edge)
H1: Mean trade return > 0 (positive edge)

t = (mean_return - 0) / (std_return / sqrt(n))

For 95% confidence:
  n=30:  t must be > 1.70
  n=50:  t must be > 1.68
  n=100: t must be > 1.66
  n=200: t must be > 1.65
```

**2. Binomial test for win rate:**
```
H0: Win rate = 50% (random)
H1: Win rate > 50%

For 60% win rate to be significant at 95%:
  Need ~70 trades minimum
For 55% win rate:
  Need ~200 trades minimum
For 52% win rate:
  Need ~600 trades minimum
```

**3. Monte Carlo bootstrap:**
- Resample trades with replacement (10,000 iterations)
- If 95% of resampled equity curves are positive, the edge is likely real

### Data Length vs Trade Frequency

| Strategy Frequency | Min Years | Rationale |
|-------------------|-----------|-----------|
| Intraday (5+ trades/day) | 2-3 years | Generates 1000+ trades quickly |
| Swing (2-5 trades/week) | 3-5 years | Need multiple market regimes |
| Positional (2-5 trades/month) | 5-8 years | Each regime must have enough trades |
| Long-term (< 1 trade/month) | 8-15 years | Very hard to get enough trades |

---

## Market Regime Definitions

### Regime Classification for Indian Markets

#### 1. Bull Market (Trending Up)
- **Definition:** Nifty 50 above its 200 DMA, making higher highs and higher lows
- **India VIX:** Typically < 18
- **Advance/Decline:** Consistently > 1.5:1
- **FII flows:** Net positive
- **Examples:** Apr 2014 - Jan 2018, Apr 2020 - Oct 2021
- **Characteristics:** Momentum strategies work, mean reversion is risky, broad participation

#### 2. Bear Market (Trending Down)
- **Definition:** Nifty 50 below its 200 DMA, making lower highs and lower lows
- **India VIX:** Typically > 22
- **Advance/Decline:** Consistently < 0.7:1
- **FII flows:** Net negative
- **Examples:** Jan 2008 - Mar 2009, Feb 2020 - Mar 2020
- **Characteristics:** Short-selling works (if allowed), defensive sectors outperform, high correlation

#### 3. Sideways/Range-Bound
- **Definition:** Nifty 50 oscillating within a 10-15% range around its 200 DMA
- **India VIX:** 12-18 (calm but uncertain)
- **Advance/Decline:** Mixed, sector rotation
- **Examples:** 2018-2019, H1 2023
- **Characteristics:** Mean reversion works, options selling strategies work, trend-following underperforms

#### 4. High Volatility (Crash/Spike)
- **Definition:** India VIX > 25, Nifty moving 2%+ daily
- **Examples:** Sep-Oct 2008, Mar 2020, Budget days with surprises
- **Characteristics:** Stop losses get hit frequently, gap risk is extreme, option premiums explode

#### 5. Low Volatility (Grind)
- **Definition:** India VIX < 13, Nifty moving < 0.5% daily for extended periods
- **Examples:** H2 2017, H2 2019
- **Characteristics:** Options decay is the dominant strategy, trend-following generates false signals

#### 6. Pre/Post Budget Period
- **Definition:** 2 weeks before and 1 week after Union Budget (typically Feb 1)
- **Characteristics:** Sector-specific moves based on expectations and announcements, high gap risk on budget day, defense/infra/rural themes dominate

#### 7. Election Cycle
- **Definition:** 6 months before and 3 months after general elections
- **Characteristics:** Uncertainty drives volatility, post-result rally (if continuity), policy-sensitive sectors (defense, infra, PSU banks) are in focus

#### 8. Monsoon Impact Period
- **Definition:** June - September
- **Characteristics:** Agriculture and rural economy stocks affected, FMCG rural sales, water/irrigation plays, monsoon deficit/surplus drives sentiment in agri stocks

#### 9. RBI Policy Cycle
- **Definition:** Rate hike or cut cycles (typically 6-12 months)
- **Characteristics:** Banking and NBFC stocks are most sensitive, bond yield curve shifts affect valuations, housing finance and auto loans impacted

#### 10. Global Crude Shock
- **Definition:** Brent crude moves >30% in a quarter
- **Characteristics:** INR weakens, OMCs (IOC, BPCL, HPCL) directly hit, paints and chemicals (crude derivatives) affected, import-heavy sectors under pressure, export sectors (IT) benefit from weak INR

---

## Common Biases

### 1. Survivorship Bias

**What it is:** Only testing on stocks that exist today, ignoring delisted/merged/bankrupt companies.

**Impact on Indian markets:**
- NSE has delisted hundreds of companies since 2000
- Companies that went bankrupt (e.g., Satyam 2009, DHFL 2019, Jet Airways) are missing from current data
- Back-testing on "current Nifty 50" misses companies that were removed
- Can inflate returns by 2-5% annually

**How to fix:**
- Use point-in-time universe data (Nifty 50 as of each rebalancing date)
- Include delisted stocks with their actual returns up to delisting
- Use databases that include survivorship-bias-free data (Bloomberg, NSE historical archives)

### 2. Look-Ahead Bias

**What it is:** Using information that was not available at the time of the trading decision.

**Common Indian market examples:**
- Using quarterly results data before they were announced
- Using index rebalancing information before the announcement date
- Using corporate action (split, bonus) adjusted prices before the ex-date
- Using FII/DII flow data before the NSDL report is published (usually T+1)

**How to fix:**
- Use point-in-time data exclusively
- Add realistic delays: fundamentals available 30 days after quarter end, FII data T+1
- Never use future price data for any calculation

### 3. Curve Fitting (Overfitting)

**What it is:** Optimizing parameters to fit historical noise rather than signal.

**How to detect:**
- Strategy only works with very specific parameter values (no plateau)
- Performance degrades dramatically with +/-10% parameter changes
- Out-of-sample performance is much worse than in-sample
- Strategy has more than 5 free parameters
- Strategy includes rules that address specific historical events

**How to fix:**
- Minimize parameters (prefer 2-3)
- Use walk-forward analysis
- Test parameter sensitivity
- Reserve 30% of data for out-of-sample testing
- Compare performance to a random strategy baseline

### 4. Data-Snooping Bias

**What it is:** Testing many strategies on the same data and selecting the best one without adjusting for multiple comparisons.

**Example:** Testing 50 indicator combinations on Nifty data, picking the one that works best, and declaring it a "strategy."

**How to fix:**
- Start with a hypothesis BEFORE testing
- Apply Bonferroni correction: divide significance threshold by number of tests
- Use separate datasets for discovery and validation
- Be honest about how many strategies you tested before finding this one

### 5. Selection Bias in Universe

**What it is:** Choosing a biased stock universe that inherently favors the strategy.

**Indian market examples:**
- Only testing on stocks that subsequently performed well
- Testing on "popular" stocks (which are popular because they went up)
- Excluding penny stocks that would have triggered entries and then lost money

**How to fix:**
- Use a predefined, rules-based universe (e.g., "all NSE stocks above Rs 100 with daily volume > 1 Cr")
- Include the full universe, even stocks that would have been bad trades
- Use index constituents as of each historical date

### 6. Execution Bias

**What it is:** Assuming perfect execution that is not achievable in practice.

**Indian market examples:**
- Assuming fills at the close price (actual close price is auction-determined)
- Ignoring circuit limits (stock at upper/lower circuit cannot be bought/sold)
- Ignoring F&O ban periods (MWPL > 95%)
- Assuming instant fills during high-volatility periods
- Not accounting for pre-open session mechanics

**How to fix:**
- Use next-candle-open for entry/exit (not current-candle-close)
- Add realistic slippage (see Slippage Modeling section)
- Code circuit limit handling (skip trade or delay)
- Model F&O ban period restrictions

---

## Walk-Forward Analysis

### The Gold Standard for Out-of-Sample Testing

Walk-forward analysis is the single most important validation technique. It simulates real-world deployment by repeatedly training and testing on different time periods.

### Step-by-Step Process

```
Total data: 2010 ---|---|---|---|---|---|---|---|---|---|---|--- 2024
                    Y1  Y2  Y3  Y4  Y5  Y6  Y7  Y8  Y9  Y10 Y11

Walk 1: Train [Y1-Y5] -----> Test [Y6-Y7]
Walk 2: Train [Y2-Y6] -----> Test [Y7-Y8]
Walk 3: Train [Y3-Y7] -----> Test [Y8-Y9]
Walk 4: Train [Y4-Y8] -----> Test [Y9-Y10]
Walk 5: Train [Y5-Y9] -----> Test [Y10-Y11]

Combined OOS: Concatenate all test periods for true performance estimate.
```

### Walk-Forward Efficiency (WFE)

```
WFE = (Average OOS Return per Walk) / (Average IS Return per Walk) x 100%
```

| WFE | Interpretation |
|-----|---------------|
| > 70% | Excellent — strategy generalizes very well |
| 50-70% | Good — acceptable level of overfitting |
| 30-50% | Fair — some overfitting, but may still be tradeable |
| < 30% | Poor — strategy is likely overfit to in-sample data |
| < 0% | Failed — strategy loses money out-of-sample |

### Indian Market Considerations for Walk-Forward

- **Structural breaks:** Indian markets had major structural changes (T+2 to T+1, algorithm trading growth, SEBI regulation changes). Walk-forward naturally handles these.
- **Regime coverage:** Ensure each test window covers at least one significant event (budget, election, global crisis).
- **Recalibration frequency:** For Indian markets, annual recalibration is typical for positional strategies; monthly for intraday.

---

## Statistical Validation

### Key Statistical Metrics

#### 1. Sharpe Ratio (India-Adjusted)
```
Sharpe = (Strategy CAGR - Risk-Free Rate) / Annualized Volatility

Risk-free rate for India: Use 91-day T-bill rate (~6-7% as of 2024)
Annualized volatility: Daily returns std x sqrt(250)
```

| Sharpe | Interpretation |
|--------|---------------|
| > 2.0 | Exceptional (verify — may be overfit) |
| 1.5-2.0 | Excellent |
| 1.0-1.5 | Good |
| 0.5-1.0 | Acceptable |
| < 0.5 | Poor — risk-adjusted returns too low |

#### 2. Calmar Ratio
```
Calmar = CAGR / Max Drawdown
```

| Calmar | Interpretation |
|--------|---------------|
| > 2.0 | Excellent |
| 1.0-2.0 | Good |
| 0.5-1.0 | Acceptable |
| < 0.5 | Poor — drawdowns too large relative to returns |

#### 3. Expectancy per Trade
```
E = (Win% x Avg Win) - (Loss% x Avg Loss)
```

This is the single most important number. It tells you how much you expect to make per trade, on average.

#### 4. System Quality Number (SQN)
```
SQN = sqrt(N) x Expectancy / StdDev(trade returns)

N = number of trades (capped at 100 for this calculation)
```

| SQN | Interpretation |
|-----|---------------|
| > 7.0 | Holy Grail (verify — likely overfit) |
| 5.0-7.0 | Superb |
| 3.0-5.0 | Excellent |
| 2.0-3.0 | Good |
| 1.5-2.0 | Below average |
| < 1.5 | Difficult to trade profitably |

#### 5. Payoff Ratio
```
Payoff = Average Win / Average Loss
```

| Win Rate | Min Payoff for Breakeven | Recommended Payoff |
|----------|------------------------|--------------------|
| 40% | 1.50 | > 2.0 |
| 50% | 1.00 | > 1.5 |
| 60% | 0.67 | > 1.0 |
| 70% | 0.43 | > 0.8 |

### Benchmark Comparison

Always compare your strategy against relevant Indian market benchmarks:

| Benchmark | When to Use |
|-----------|------------|
| Nifty 50 TRI | Default for large-cap strategies |
| Nifty Midcap 150 TRI | Midcap strategies |
| Nifty Smallcap 250 TRI | Smallcap strategies |
| Nifty 500 TRI | Broad market strategies |
| Fixed Deposit (7%) | Absolute return benchmark |
| Buy-and-hold the universe | Most relevant — shows if active management adds value |

**TRI = Total Return Index** (includes dividends). Always use TRI for benchmark comparison, not the price index.
