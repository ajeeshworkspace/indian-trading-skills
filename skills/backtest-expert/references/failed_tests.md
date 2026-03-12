# Failed Backtests — Patterns, Red Flags, and Documentation Framework

## Why Failed Backtests Are Valuable

> "Every failed backtest narrows the search space. The trader who has tested and rejected 50 strategies knows far more than the one who deployed the first thing that 'looked good.'"

A properly documented failed backtest:
1. **Prevents repeating mistakes** — you will not re-test the same idea 6 months later
2. **Reveals market structure** — failures often point to real market mechanics
3. **Builds intuition** — pattern recognition for what works and what does not
4. **Saves time** — a quick reference before starting a new strategy
5. **Informs related strategies** — a failed momentum strategy might reveal a mean-reversion edge

---

## Common Failure Patterns

### Pattern 1: The Cost Killer

**Symptoms:**
- Strategy looks profitable before transaction costs
- After adding brokerage + STT + slippage, expectancy goes to zero or negative
- High trade frequency (5+ trades/day)

**Why it happens:**
- Indian delivery trading costs ~0.3-0.5% round-trip
- Even intraday costs ~0.1-0.2% round-trip
- A strategy with 0.15% average profit per trade cannot survive 0.2% costs

**Common Indian market examples:**
- Scalping strategies on mid-cap stocks (spreads too wide)
- Options buying strategies with small targets (premium decay + costs eat the edge)
- Pair trading on illiquid stock pairs (slippage on both legs)

**Lesson:** Calculate the minimum edge needed to cover costs BEFORE backtesting.

```
Minimum edge per trade:
  Delivery: > 0.5% (to cover costs + provide profit)
  Intraday: > 0.2%
  F&O options: > 1-2% of premium
  F&O futures: > 0.1%
```

---

### Pattern 2: The Parameter Peak

**Symptoms:**
- Excellent results at exact parameter values (e.g., RSI=42, EMA=17)
- Performance collapses with even small changes (+/-10%)
- Heat map shows a narrow spike, not a plateau
- Out-of-sample performance is much worse than in-sample

**Why it happens:**
- The optimizer found noise, not signal
- With enough parameters and enough data, you can always fit a profitable curve
- The "optimal" parameters are describing past noise, not a repeatable edge

**Red flag math:**
```
If you test 100 parameter combinations, ~5 will appear "significant" at the 95%
confidence level purely by chance. This is data snooping.
```

**Lesson:** Always check parameter sensitivity before celebrating good results.

---

### Pattern 3: The Regime Specialist

**Symptoms:**
- Strategy performs brilliantly in one market regime (e.g., 2020-2021 bull run)
- Flat or negative in other regimes
- Often discovered by testing on a specific "exciting" period

**Indian market examples:**
- Momentum strategy trained on 2020-2021 (everything went up)
- Mean-reversion strategy trained on 2018-2019 (sideways market)
- Short-selling strategy trained on Feb-Mar 2020 (COVID crash)

**Why it happens:**
- The strategy captures a regime-specific pattern, not a universal edge
- The regime may not repeat, or may repeat with different characteristics

**Lesson:** A strategy must survive at least 3 different market regimes to be deployable.

---

### Pattern 4: The Survivorship Illusion

**Symptoms:**
- Strategy has high returns because it only trades stocks that are still listed
- Stocks that went bankrupt, were delisted, or hit lower circuits are excluded
- Back-tested universe is the "current" Nifty 200

**Indian market examples:**
- Strategy: "Buy all stocks that fell >50% and hold for recovery"
- Back-tested on current universe: Works great (survivors recovered)
- Reality: Many stocks that fell >50% never recovered (DHFL, Jet Airways, Satyam, Yes Bank below Rs 20)

**Lesson:** Always use point-in-time universe data. Include delisted stocks.

---

### Pattern 5: The Circuit Limit Trap

**Symptoms:**
- Strategy uses stop losses that assume you can exit at any price
- In reality, stocks hit lower circuit and no exit is possible
- A few circuit-limit events cause catastrophic losses

**Indian market specifics:**

| Category | Circuit Limit | Impact |
|----------|--------------|--------|
| Stocks in derivative segment | No circuit for F&O stocks | Price can move freely |
| Stocks NOT in derivative segment | 5%, 10%, 15%, 20% | Cannot exit if at lower circuit |
| Index | N/A (no index circuit, but market-wide circuit exists) | Trading halt at 10%, 15%, 20% Nifty move |

**Real examples:**
- Small-cap stocks frequently hit lower circuit for 3-5 consecutive days
- Post-earnings gaps can lock stocks at circuit for the entire session
- During market panics (March 2020), many stocks hit lower circuit simultaneously

**Lesson:** If your strategy trades non-F&O stocks, you MUST model circuit limit behavior. Either:
1. Skip non-F&O stocks entirely
2. Add circuit-limit handling (delay exit, accept slippage)
3. Stress test with 2-3 day exit delays

---

### Pattern 6: The Gap Risk Destroyer

**Symptoms:**
- Strategy works well during market hours
- Overnight gaps cause unexpected losses
- Stop loss is 2%, but stock gaps down 8% on bad earnings

**Indian market gap risk factors:**
- Quarterly results (usually announced after market hours)
- Global market moves (Nifty correlates with US markets, which trade after Indian close)
- RBI policy announcements (sometimes mid-session)
- Government policy changes (tariffs, taxes, regulations)
- Rating agency downgrades
- SEBI actions (stock-specific)

**Typical gap magnitudes:**
| Event | Typical Gap | Extreme Gap |
|-------|-------------|-------------|
| Earnings miss | -3% to -8% | -15% to -20% |
| Earnings beat | +3% to +8% | +10% to +15% |
| Global sell-off (overnight) | -1% to -3% | -5% to -10% |
| Government policy | -2% to +2% | -5% to +5% |
| Rating downgrade | -3% to -10% | -15%+ |
| Fraud/scandal | -10% to -30% | -50%+ (circuit) |

**Lesson:** If your strategy holds positions overnight, gap risk is your biggest unmodeled risk. Either:
1. Close all positions intraday (eliminates gap risk but limits strategy types)
2. Model gaps explicitly (use historical gap data)
3. Size positions assuming your stop loss will be exceeded by 2-3x on gaps

---

### Pattern 7: The F&O Ban Period Blow-Up

**Symptoms:**
- Strategy trades stocks in F&O segment
- Does not account for ban period restrictions
- During ban periods, cannot enter new positions, forced to close losing ones

**What is F&O ban?**
- When open interest in a stock crosses 95% of Market Wide Position Limit (MWPL)
- No new F&O positions allowed (can only close existing ones)
- Stock moves can be extreme during ban period (short squeeze)
- Ban can last days or weeks

**Recent examples of stocks frequently hitting ban:**
- IDEA (Vodafone Idea) — frequent ban periods
- PNB — during NPA crisis
- Various midcap stocks during momentum phases

**Lesson:** If trading stock F&O, always check MWPL status and handle ban periods in backtest code.

---

### Pattern 8: The Liquidity Mirage

**Symptoms:**
- Strategy shows good results on backtested data
- In live trading, cannot get fills at backtested prices
- Especially problematic for options strategies

**Indian market liquidity realities:**
- Nifty and Bank Nifty options: Liquid at ATM, illiquid 5+ strikes away
- Stock options: Generally illiquid except top 20-30 names
- Stock futures: Liquid for current month, illiquid for next month
- Small-cap stocks: Can have zero bid for minutes at a time
- Pre-market and post-market: Very thin liquidity

**Lesson:** Check average daily volume and typical bid-ask spread for every instrument in your universe. If your order would be >1% of daily volume, you will move the market.

---

## Case Study Documentation Framework

When a backtest fails, document it using this template to build your knowledge base.

### Template

```markdown
# Failed Backtest: [Strategy Name]

## Date: [YYYY-MM-DD]

## Hypothesis
[One-sentence statement of the expected edge]

## Rules
- Universe: [what stocks/instruments]
- Entry: [exact conditions]
- Exit: [target, stop, time-based]
- Position sizing: [how much per trade]
- Parameters: [list all free parameters with values]

## Backtest Period
- In-sample: [start] to [end]
- Out-of-sample: [start] to [end]
- Total trades: [number]

## Results Summary
| Metric | In-Sample | Out-of-Sample |
|--------|-----------|---------------|
| CAGR | | |
| Sharpe | | |
| Max DD | | |
| Win Rate | | |
| Profit Factor | | |
| Expectancy/trade | | |

## Why It Failed
[Primary failure pattern from the list above]

## Detailed Analysis
[What specifically went wrong, with data]

## What I Learned
[Key insight that applies to future strategies]

## Related Ideas
[Did the failure suggest a different approach?]

## Score (from evaluate_backtest.py)
[Paste the evaluation output]
```

---

## Red Flags Checklist

Use this checklist before committing capital to any strategy. A single "critical" red flag should prevent deployment. Three or more "warning" flags should trigger a re-evaluation.

### Critical Red Flags (Do NOT deploy)

- [ ] **Negative expectancy after costs** — The strategy loses money on average per trade when realistic costs are included
- [ ] **Fewer than 30 trades** — No statistical basis for any claim
- [ ] **More than 5 free parameters** — Almost certainly overfit
- [ ] **Slippage and costs not modeled** — Results are fantasy, not estimates
- [ ] **Look-ahead bias detected** — Using information not available at trade time
- [ ] **Survivorship bias in universe** — Only tested on currently listed stocks
- [ ] **No out-of-sample test** — In-sample results are meaningless alone
- [ ] **Strategy only works in one regime** — It will fail when the regime changes

### Warning Red Flags (Proceed with extreme caution)

- [ ] **Win rate above 80%** — Verify fills and check for bias
- [ ] **CAGR above 50%** — Extraordinary claims require extraordinary evidence
- [ ] **No losing months in 3+ years** — Something is wrong with the data
- [ ] **Max drawdown below 5%** — Unrealistic for any strategy with meaningful returns
- [ ] **Only 30-100 trades** — Directional evidence only, wide confidence intervals
- [ ] **Less than 5 years tested** — May miss important regime changes
- [ ] **Drawdown above 30%** — Most traders will abandon the strategy before recovery
- [ ] **Walk-forward efficiency below 50%** — Significant overfitting present
- [ ] **Average loss > 2x average win** — Fragile risk/reward structure
- [ ] **Strategy requires overnight/weekly holding of small-caps** — Gap and circuit risk
- [ ] **Strategy trades illiquid instruments** — Execution will deviate from backtest

### Info Flags (Be aware)

- [ ] **Strategy is purely technical** — Consider if fundamental overlay would help
- [ ] **Strategy has no benchmark comparison** — May just be buying the market with leverage
- [ ] **Strategy only tested on Nifty 50 universe** — Try Nifty 200 or 500 for robustness
- [ ] **No Monte Carlo simulation** — Single-path results can be misleading
- [ ] **No paper trading phase planned** — Skip at your own risk

---

## Indian Market-Specific Failure Scenarios

### 1. Budget Day Surprise

**Scenario:** Strategy is fully invested going into Budget Day (February 1). An unexpected policy change causes a 3-5% gap against positions.

**Affected strategies:** All positional strategies that do not reduce exposure before Budget.

**Mitigation:**
- Reduce position size by 50% 2 days before Budget
- Tighten stops by 50%
- OR: Close all positions before Budget and re-enter after

### 2. Election Result Volatility

**Scenario:** General election results are announced. If unexpected, Nifty can move 5-8% in a single session.

**Affected strategies:** Any strategy holding overnight positions during election week.

**Mitigation:**
- Go flat or reduce to 25% exposure during election result week
- Use options hedges (puts if long)
- Accept that this is an unmodeled risk if holding positions

### 3. RBI Surprise Rate Action

**Scenario:** RBI changes rates unexpectedly (outside normal policy meeting or by an unexpected quantum).

**Affected strategies:** Strategies trading banks, NBFCs, housing finance, auto.

**Mitigation:**
- Check RBI calendar and reduce banking-sector exposure around policy dates
- Use sector-neutral strategies that are not rate-sensitive

### 4. Global Contagion (FII Selling Pressure)

**Scenario:** Global risk-off event causes FIIs to sell Rs 3,000-5,000 Cr per day for 10+ consecutive days.

**Affected strategies:** All long-only strategies, especially in FII-heavy large-caps.

**Mitigation:**
- Monitor FII flow data daily (available T+1 from NSDL)
- Reduce exposure when FII selling exceeds Rs 2,000 Cr/day for 3+ days
- Diversify into DII-supported sectors (PSU banks, infrastructure)

### 5. Stock-Specific Corporate Governance Failure

**Scenario:** Fraud or governance issue discovered (Satyam 2009, DHFL 2019, Adani Group 2023).

**Affected strategies:** Concentrated strategies with large single-stock exposure.

**Mitigation:**
- Maximum 5% per stock (10% for very high conviction)
- Diversify across at least 10-15 stocks
- Use forensic accounting screens (e.g., Beneish M-Score, cash flow vs reported profit)
- This is fundamentally unhedgeable — position sizing is your only defense

### 6. NSE System Outage

**Scenario:** NSE systems go down during trading hours (happened February 2021 for ~3.5 hours).

**Affected strategies:** Intraday strategies that need to close positions before market close.

**Mitigation:**
- Have BSE as a backup exchange for critical exits
- Size positions assuming you may not be able to exit for a full session
- Intraday strategies: Use MIS product type (broker will auto-square-off)

---

## Key Takeaways

1. **Document every failure.** Your failed-backtest library is more valuable than your strategy library.
2. **Look for patterns in failures.** If 5 momentum strategies failed due to transaction costs, the insight is: "momentum works but only at low frequency."
3. **Share failures (anonymized).** The trading community benefits more from shared failures than shared successes.
4. **Re-visit failures periodically.** Market structure changes. A strategy that failed in 2018 might work in 2025 due to changed microstructure.
5. **Use the evaluation script.** `python3 evaluate_backtest.py` gives an objective score that removes emotional attachment to a strategy.
