# Indian F&O Market Reference Guide

A comprehensive reference for options strategy advisors working with NSE Futures &
Options. This document covers market structure, regulations, costs, and practical
trading considerations specific to the Indian derivatives market.

---

## Table of Contents

1. [NSE F&O Market Structure](#1-nse-fo-market-structure)
2. [SEBI Margin Framework](#2-sebi-margin-framework)
3. [STT and Transaction Charges](#3-stt-and-transaction-charges)
4. [European vs American Exercise](#4-european-vs-american-exercise)
5. [Weekly vs Monthly Expiry Strategies](#5-weekly-vs-monthly-expiry-strategies)
6. [OI-Based Support and Resistance](#6-oi-based-support-and-resistance)
7. [Max Pain Theory for Indian Expiry](#7-max-pain-theory-for-indian-expiry)
8. [India VIX and Option Premiums](#8-india-vix-and-option-premiums)
9. [F&O Ban Mechanism](#9-fo-ban-mechanism)
10. [Common Strategies for Indian Traders](#10-common-strategies-for-indian-traders)
11. [Position Sizing for Indian F&O](#11-position-sizing-for-indian-fo)
12. [Rollover Strategies Near Expiry](#12-rollover-strategies-near-expiry)

---

## 1. NSE F&O Market Structure

### Contract Specifications

#### Index Options

| Parameter       | NIFTY 50        | BANK NIFTY      | FINNIFTY        | MIDCAP NIFTY    |
|-----------------|-----------------|-----------------|-----------------|-----------------|
| Lot Size        | 75 (verify)     | 15 (verify)     | 25              | 50              |
| Tick Size       | 0.05            | 0.05            | 0.05            | 0.05            |
| Strike Interval | 50              | 100             | 50              | 25              |
| Expiry          | Weekly (Thu)    | Weekly (Wed)    | Weekly (Tue)    | Monthly (Mon)   |
| Settlement      | Cash            | Cash            | Cash            | Cash            |
| Exercise        | European        | European        | European        | European        |

Note: Lot sizes are revised periodically by the exchange. Always verify the current
lot size using `fno_mcx_contracts_search_tool` before trading.

#### Stock Options

| Parameter       | Value                                          |
|-----------------|------------------------------------------------|
| Lot Size        | Varies by stock (set by exchange)              |
| Tick Size       | 0.05                                           |
| Strike Interval | Varies by stock price level                    |
| Expiry          | Monthly only (last Thursday of the month)      |
| Settlement      | Physical delivery (shares change hands)        |
| Exercise        | European                                       |

#### Futures Contracts

| Parameter       | Index Futures   | Stock Futures   |
|-----------------|-----------------|-----------------|
| Contract Months | Near, Next, Far | Near, Next, Far |
| Lot Size        | Same as options | Same as options |
| Settlement      | Cash (daily MTM)| Physical (at expiry) |
| Last Trading Day| Last Thursday of expiry month                  |

### Trading Hours

| Session         | Time (IST)       |
|-----------------|------------------|
| Pre-Open        | 09:00 - 09:08    |
| Normal Trading  | 09:15 - 15:30    |
| Post-Close      | 15:40 - 16:00    |

### Expiry Schedule

- **NIFTY:** Every Thursday (weekly) + last Thursday of month (monthly)
- **BANK NIFTY:** Every Wednesday (weekly) + last Wednesday of month (monthly)
- **FINNIFTY:** Every Tuesday (weekly)
- **SENSEX (BSE):** Every Friday (weekly)
- **Stock Options:** Last Thursday of month only
- **Stock Futures:** Last Thursday of month

If the scheduled expiry day is a trading holiday, the expiry moves to the
preceding trading day.

### Available Strikes

The exchange lists strikes around the current spot price in predefined intervals.
As the underlying moves, new strikes are added. Strikes well away from the
current price (deep OTM or deep ITM) may have very low liquidity.

---

## 2. SEBI Margin Framework

SEBI's margin framework for F&O trading consists of multiple components designed
to cover different types of risk.

### Margin Components

#### 1. SPAN Margin (Initial Margin)

SPAN (Standard Portfolio Analysis of Risk) calculates the worst-case loss of a
portfolio over a one-day time horizon. It considers:

- Price scanning range (based on volatility)
- Up and down movements in the underlying
- Changes in volatility
- Time decay
- Correlation between instruments (for portfolio margining)

SPAN margin is recalculated multiple times during the trading day.

#### 2. Exposure Margin

An additional margin collected over and above SPAN to cover risks not captured
by SPAN:

- **Index derivatives:** 3% of the notional value of the contract
- **Stock derivatives:** Higher of 5% or 1.5 standard deviations of the
  logarithmic returns of the stock over the last 6 months

#### 3. Premium Margin (for Option Buyers)

Option buyers pay the full premium upfront. This is not a margin in the
traditional sense but the cost of the option position.

#### 4. Assignment Margin

Collected from option sellers who are assigned. Covers the settlement obligation.

### Peak Margin Requirement

Since September 2021, SEBI mandates **peak margin** collection:

- Brokers must collect margins based on the peak (highest) margin required
  during the trading day, not just the end-of-day margin.
- The clearing corporation takes at least 4 random snapshots during the day.
- If a client's margin falls below the peak requirement, a penalty is levied.
- This means intraday positions also require full margin.

### Margin for Multi-Leg Strategies

For hedged positions (spreads, iron condors, etc.), SPAN recognizes the hedge
benefit and reduces the margin requirement compared to naked positions. However,
the margin benefit is only available if both legs are in the same expiry.

For example:
- **Naked short NIFTY call:** Requires full SPAN + exposure margin (often
  Rs. 1,00,000+ per lot).
- **Bear Call Spread (short call + long call):** Margin is significantly lower
  because the long call limits the maximum loss.

Use `calculate_fno_margin` to get the exact margin for any combination.

### Margin Penalty

If the client's margin falls short of the required margin:

| Shortfall                | Penalty                      |
|--------------------------|------------------------------|
| Up to 10% of required   | 0.5% per day of shortfall    |
| More than 10%            | 1.0% per day of shortfall    |

Penalties are levied per day and compounded for repeat offenses within a month.

---

## 3. STT and Transaction Charges

### Securities Transaction Tax (STT)

STT is a tax levied by the government on securities transactions.

| Transaction               | STT Rate                    | Levied On        |
|---------------------------|-----------------------------|------------------|
| Futures (sell)            | 0.0125%                     | Sell turnover     |
| Options (sell)            | 0.0625%                     | Sell premium      |
| Options (exercise at expiry, ITM) | 0.0625%            | Intrinsic value   |

**Critical STT Trap for Options:**
When an option expires in-the-money (ITM), STT is levied on the entire
intrinsic value (settlement value), not just the premium. This can result in
STT exceeding the actual profit.

Example:
- You sell a NIFTY 24000 CE at Rs. 5 (premium received: 5 x 75 = Rs. 375).
- NIFTY expires at 24010 (option is ITM by Rs. 10).
- Intrinsic value on exercise: 10 x 75 = Rs. 750.
- STT on exercise: 0.0625% of Rs. 750 = Rs. 0.47 per share = Rs. 35.16.
- But if NIFTY expires at 24200, intrinsic value = 200 x 75 = Rs. 15,000.
- STT = 0.0625% of Rs. 15,000 = Rs. 9.38.

For deep ITM options at expiry, this tax can be substantial. Always square off
ITM positions before expiry to avoid the exercise-based STT.

### Other Transaction Charges

| Charge                    | Rate (approximate)          |
|---------------------------|-----------------------------|
| Exchange Transaction Fee  | ~0.05% (NSE)                |
| SEBI Turnover Fee         | Rs. 10 per crore            |
| GST                       | 18% on brokerage + fees     |
| Stamp Duty                | 0.003% (buy side) for options|

### Total Cost Per Trade (Approximate)

For a typical NIFTY option trade (1 lot, premium Rs. 100):
- Brokerage: Rs. 20 (flat per order, typical discount broker)
- STT: Rs. 4.69 (on sell)
- Exchange charges: Rs. 3.97
- GST: Rs. 4.31
- SEBI fee: Rs. 0.08
- Stamp duty: Rs. 0.23
- **Total: approximately Rs. 33 per side**

---

## 4. European vs American Exercise

### All NSE Options Are European

Since 2010, all options on NSE (both index and stock) are European-style. This
means:

- **Cannot exercise before expiry.** The option can only be exercised (or is
  auto-exercised) at expiry.
- **No early exercise risk for sellers.** Sellers do not need to worry about
  being assigned before expiry.
- **Time value is always retained.** Unlike American options where early exercise
  can strip time value, European options always trade with full time value intact.

### Implications for Pricing

- **Black-Scholes model applies directly.** No need for binomial trees or
  American option adjustments. The closed-form Black-Scholes formula is exact
  for European options.
- **Put-Call Parity holds exactly:**
  ```
  Call - Put = S * exp(-q*T) - K * exp(-r*T)
  ```
  where S = spot, K = strike, r = risk-free rate, q = dividend yield, T = time.

- **No early exercise premium.** American options sometimes carry a premium
  (especially deep ITM puts) because of the early exercise feature. European
  options have no such premium.

### Implications for Strategies

- **Covered call sellers:** No risk of early assignment. The short call will
  only be exercised at expiry.
- **Calendar spreads:** Work cleanly because both legs follow European rules.
- **Deep ITM options:** May trade at a slight discount to intrinsic value
  (unlike American options which always trade at or above intrinsic). This is
  because you cannot exercise early to capture the intrinsic value.

---

## 5. Weekly vs Monthly Expiry Strategies

### Weekly Expiry Characteristics

| Feature              | Weekly                    | Monthly                    |
|----------------------|---------------------------|----------------------------|
| Time to Expiry       | 0-7 days                  | 0-30+ days                 |
| Theta Decay          | Very rapid (accelerating) | Gradual (more predictable) |
| Gamma Risk           | Extremely high near expiry| Moderate                   |
| Premium              | Lower (less time value)   | Higher                     |
| Liquidity            | High for index options    | High for all               |
| Available For        | Index options only        | All stocks and indices     |

### Weekly Expiry Strategies

#### 1. Short Straddle / Strangle on Expiry Day

The most popular strategy among Indian traders for weekly expiry:

- Sell ATM straddle or OTM strangle on the expiry morning (or 1-2 days before).
- Benefit from accelerated theta decay in the final hours.
- Risk: Gamma is extremely high, meaning a small move in the underlying causes
  a large change in delta and hence P&L.

**Typical approach:**
- Sell straddle at 9:15 AM on expiry day.
- Set stop-loss at 1.5x to 2x of premium received.
- Close position by 2:30 PM or let expire.
- Monitor continuously for sharp moves.

#### 2. Iron Condor for Range Days

- Deploy iron condor 1-2 days before expiry.
- Choose strikes based on expected range (use OI data for support/resistance).
- Benefit from rapid decay with defined risk.

#### 3. Directional Plays with Weekly Options

- Buy weekly OTM options when expecting a large move (event-based).
- Very cheap premium but high risk of total loss.
- Best used for asymmetric bets (small risk, large potential reward).

### Monthly Expiry Strategies

#### 1. Positional Strategies

- Deploy strategies 15-25 days before monthly expiry.
- Allow time for the thesis to play out.
- More stable Greeks compared to weekly options.

#### 2. Earnings-Based Plays

- Stock options are monthly only, so earnings plays use monthly expiry.
- Long straddle/strangle before earnings announcement.
- Short straddle/strangle after earnings if IV crush is expected.

#### 3. Rollover Period Strategies

- In the last week before monthly expiry, rollover activity creates opportunities.
- Open interest shifts from current month to next month.
- Basis (difference between futures and spot) widens or narrows, creating
  spread trading opportunities.

---

## 6. OI-Based Support and Resistance

### Interpreting Open Interest

Open Interest (OI) represents the total number of outstanding derivative
contracts that have not been settled.

#### Call OI = Resistance

When a large amount of call OI builds up at a particular strike, it suggests
that:
- Many traders have sold (written) calls at that strike.
- These writers will actively defend their position by selling the underlying
  near that level.
- This creates overhead resistance for the underlying.

Example: If NIFTY 24500 CE has the highest call OI, 24500 is likely to act
as resistance.

#### Put OI = Support

When a large amount of put OI builds up at a particular strike:
- Many traders have sold (written) puts at that strike.
- These writers will defend their position by buying the underlying near that level.
- This creates support for the underlying.

Example: If NIFTY 23500 PE has the highest put OI, 23500 is likely to act
as support.

### Put-Call Ratio (PCR)

PCR = Total Put OI / Total Call OI

| PCR Range     | Interpretation                                        |
|---------------|-------------------------------------------------------|
| PCR > 1.3     | Very bullish (excessive put writing = strong support)  |
| 1.1 - 1.3     | Moderately bullish                                    |
| 0.9 - 1.1     | Neutral                                               |
| 0.7 - 0.9     | Moderately bearish                                    |
| PCR < 0.7     | Very bearish (excessive call writing = strong ceiling) |

**Contrarian interpretation:** Extreme PCR values can also signal reversals:
- Very high PCR (> 1.5): Market may be over-hedged, potential for short covering rally.
- Very low PCR (< 0.5): Market may be complacent, potential for downside.

### Change in OI Analysis

More informative than absolute OI is the change in OI during the day:

| Price Move | OI Change | Interpretation        |
|------------|-----------|----------------------|
| Up         | Increase  | Long buildup (bullish)|
| Up         | Decrease  | Short covering (less bullish) |
| Down       | Increase  | Short buildup (bearish)|
| Down       | Decrease  | Long unwinding (less bearish)|

Use `get_open_interest_analysis` with `view='change_in_oi'` to get intraday OI
change data.

### Practical OI Analysis Workflow

1. Call `get_open_interest_analysis(symbol="NIFTY", view="all")` to get full picture.
2. Identify the strikes with highest call OI (resistance) and put OI (support).
3. Check PCR for directional bias.
4. Use `view='change_in_oi'` to see if OI is building or unwinding during the day.
5. Combine with price action and VIX for strategy selection.

---

## 7. Max Pain Theory for Indian Expiry

### What is Max Pain?

Max Pain is the strike price at which the maximum number of options contracts
(calls + puts combined) expire worthless. At this point, option buyers lose the
most money and option sellers (writers) pay out the least.

### Calculation

For each strike price:
1. Calculate the total value of all call options that would be ITM if the
   underlying settled at that strike.
2. Calculate the total value of all put options that would be ITM if the
   underlying settled at that strike.
3. Add call pain + put pain = total pain at that strike.
4. The strike with the minimum total pain is the Max Pain strike.

### Max Pain in Indian Markets

Max Pain is particularly relevant for Indian weekly expiry because:

1. **Large option writing community:** India has a massive number of retail
   option sellers. These sellers collectively have an interest in the underlying
   settling near max pain.

2. **Weekly expiry concentration:** A disproportionate amount of OI is
   concentrated in weekly options, making max pain more influential.

3. **Hedging activity by institutional writers:** When the underlying moves away
   from max pain, institutional option sellers hedge by buying/selling the
   underlying or futures, which pushes the price back toward max pain.

4. **Empirical observation:** NIFTY weekly expiry often settles within 50-100
   points of the max pain strike, especially on low-volatility days.

### Trading with Max Pain

- **Before expiry (2-3 days):** If the underlying is far from max pain, expect
  a gravitational pull toward max pain.
- **On expiry day:** If the underlying is near max pain, deploy range-bound
  strategies (iron condor, short strangle).
- **Deviation from max pain:** Strong trend days or event-driven moves can
  override max pain. Do not rely on max pain alone.

### Limitations

- Max pain shifts throughout the week as OI changes.
- On high-volatility days, max pain is less reliable.
- It is a tendency, not a certainty. Use it as one data point among many.

---

## 8. India VIX and Option Premiums

### What is India VIX?

India VIX (Volatility Index) measures the market's expectation of volatility
over the next 30 calendar days. It is computed from NIFTY option prices using
a model-free approach similar to the CBOE VIX methodology.

- **India VIX is expressed as an annualized percentage.**
- India VIX of 15 means the market expects NIFTY to move approximately
  15% / sqrt(12) = ~4.3% over the next month.
- For a daily expected move: India VIX / sqrt(252).

### VIX Levels and Interpretation

| VIX Level | Market Regime    | Strategy Implications                     |
|-----------|------------------|-------------------------------------------|
| < 12      | Very low vol     | Sell options cautiously; premiums are thin |
| 12 - 15   | Low vol          | Favor selling strategies (iron condor)     |
| 15 - 20   | Normal           | Balanced approach; both buying and selling |
| 20 - 25   | Elevated         | Premiums are rich; selling is attractive    |
| 25 - 35   | High vol         | Selling is lucrative but risky; wide stops |
| > 35      | Crisis/Panic     | Extreme caution; only defined-risk trades  |

### VIX-Premium Relationship

- **VIX rising:** Option premiums increase across all strikes. Sellers receive
  more premium but face higher risk. Buyers pay more but have higher probability
  of a profitable move.
- **VIX falling (IV crush):** Option premiums shrink. This is painful for option
  buyers and beneficial for sellers.

### Common VIX Patterns in India

1. **Pre-budget spike:** VIX typically rises 5-10 points in the 2-3 days before
   the Union Budget and crashes 3-5 points immediately after.
2. **Pre-election volatility:** VIX can spike to 25-35 before general election
   results and crash dramatically after results.
3. **RBI MPC meetings:** Moderate VIX increase before policy decisions, quick
   normalization after.
4. **Global events:** VIX correlates with global volatility (US VIX, geopolitical
   events).

### Using VIX for Strategy Selection

- **VIX > 20 and you are selling options:** Collect premium but use defined-risk
  strategies (iron condor, spreads) rather than naked selling.
- **VIX < 13 and you are buying options:** Premiums are cheap; good for
  directional bets or straddles before expected events.
- **VIX dropping sharply:** If you have long option positions, close them quickly
  to avoid IV crush losses.
- **VIX at extremes:** Mean reversion is likely. VIX above 30 tends to revert;
  VIX below 10 tends to rise.

---

## 9. F&O Ban Mechanism

### What is F&O Ban?

When the aggregate open interest in all F&O contracts of a particular stock
exceeds 95% of the Market-Wide Position Limit (MWPL), the stock enters an
F&O ban period.

### MWPL Calculation

MWPL = 20% of the free-float market capitalization of the stock
(expressed in number of shares and then converted to the nearest lot size).

### Ban Rules

1. **Entry into ban:** OI > 95% of MWPL. The exchange announces the ban,
   effective from the next trading day.
2. **During ban:**
   - No new F&O positions can be created (no fresh buying or selling).
   - Only squaring off (closing) of existing positions is allowed.
   - Any order that would increase OI is rejected by the exchange.
3. **Exit from ban:** OI drops below 80% of MWPL. The ban is lifted from the
   next trading day.
4. **Penalty for violating ban:** If a trader increases positions during the ban
   period, a penalty of 1% of the value of the increased position per day is
   levied (minimum Rs. 5,000 to maximum Rs. 1,00,000).

### Stocks Commonly Under F&O Ban

Stocks with lower free-float capitalization or those experiencing speculative
activity are more prone to F&O bans. Examples include mid-cap stocks with
active F&O trading.

### Impact on Strategies

- **Before ban:** If OI is approaching 90% MWPL, be cautious about entering
  new positions. Existing positions can become illiquid.
- **During ban:** You can only exit. This may lead to wider bid-ask spreads
  and difficulty closing at fair prices.
- **Approaching ban exit:** As OI decreases toward 80%, traders start to
  position for the ban lift, which can create trading opportunities.

### Monitoring

Always check if a stock is near the ban threshold before deploying strategies.
The exchanges publish daily MWPL utilization reports. Groww MCP tools can help
identify stocks in or near ban.

---

## 10. Common Strategies for Indian Traders

### Strategy 1: Nifty Short Straddle on Thursday Expiry

**Setup:**
- Sell NIFTY ATM CE + ATM PE on Thursday morning (expiry day).
- Or deploy 1-2 days before expiry for more premium.

**Rationale:**
- Theta decay is fastest on expiry day.
- NIFTY tends to settle near max pain on non-event days.

**Risk Management:**
- Stop-loss at 1.5x-2x premium received on either side.
- Adjust by adding a hedge leg (convert to strangle by shifting the losing side).
- Maximum loss should not exceed 3% of capital.

**Capital Required:** SPAN + Exposure margin for 2 naked option legs (typically
Rs. 1,50,000 - Rs. 2,00,000 per lot for the straddle).

### Strategy 2: Bank Nifty Iron Condor on Wednesday Expiry

**Setup:**
- Sell OTM Call + Sell OTM Put.
- Buy further OTM Call + Buy further OTM Put (wings for protection).
- Deploy 1-2 days before Wednesday expiry.

**Rationale:**
- Bank Nifty is more volatile than Nifty, so premiums are richer.
- Iron condor provides defined risk unlike naked straddles.

**Risk Management:**
- Max loss is limited to (strike width - net credit) x lot size.
- Exit if underlying breaches the short strikes.

**Capital Required:** Reduced margin due to hedged position (typically
Rs. 50,000 - Rs. 80,000 per lot).

### Strategy 3: Event-Day Long Straddle (Budget/RBI/Elections)

**Setup:**
- Buy ATM Straddle 2-3 days before the event.
- Choose monthly expiry to avoid extreme theta decay.

**Rationale:**
- VIX spikes before events, but the actual move can exceed the premium paid.
- Elections and budgets can cause 2-5% moves in Nifty.

**Risk Management:**
- Maximum loss is the total premium paid.
- Set a target of 1.5x-2x premium paid for exit.
- Close immediately after the event (within the first hour) to capture the move
  before IV crush sets in.

**Capital Required:** Premium paid upfront (no margin since buyer).

### Strategy 4: Covered Call with Futures

**Setup:**
- Buy 1 lot of NIFTY futures.
- Sell 1 lot of OTM NIFTY call option (same expiry).

**Rationale:**
- Generate income on the long futures position.
- OTM call sold provides a buffer against small declines.

**Risk Management:**
- Downside risk is the futures P/L minus the call premium received.
- Roll the short call to the next expiry if not exercised.

**Capital Required:** Futures margin + reduced margin for the covered call
(hedge benefit).

### Strategy 5: Calendar Spread (Weekly-to-Monthly)

**Setup:**
- Sell current week ATM option (weekly expiry).
- Buy next month ATM option (monthly expiry).

**Rationale:**
- Near-week option decays faster than the far-month option.
- Net theta is positive (earning from time decay difference).

**Risk Management:**
- If the underlying moves sharply, both legs move similarly and net P/L is small.
- Close the short leg at expiry and either close the long leg or sell a new
  short leg against it.

**Capital Required:** The net debit of the spread plus any margin requirement
for the short leg.

---

## 11. Position Sizing for Indian F&O

### Per-Lot Risk Approach

The safest approach to position sizing is to calculate risk per lot and size
positions based on a fixed percentage of capital at risk.

#### Step-by-Step Process

1. **Determine total trading capital** allocated to F&O.
2. **Set maximum risk per trade:** 1-2% of total capital for beginners,
   3-5% for experienced traders.
3. **Calculate risk per lot** for the chosen strategy:
   - For defined-risk strategies (spreads, iron condors): Max loss = (strike
     width - net credit) x lot size.
   - For undefined-risk strategies (naked options): Use the stop-loss amount
     as the risk per lot.
4. **Number of lots = Maximum risk per trade / Risk per lot.**

#### Example

- Trading capital: Rs. 10,00,000
- Maximum risk per trade: 2% = Rs. 20,000
- Strategy: Nifty Iron Condor
  - Short put: 23800, Long put: 23500 (width = 300)
  - Short call: 24200, Long call: 24500 (width = 300)
  - Net credit: Rs. 80 per share
  - Max loss per lot: (300 - 80) x 75 = Rs. 16,500
- Number of lots: 20,000 / 16,500 = 1.21 -> trade 1 lot.

### Capital Allocation Guidelines

| Capital Range         | Recommended Approach                           |
|-----------------------|------------------------------------------------|
| < Rs. 2,00,000        | Only buy options (no writing). 1-2 lots max.  |
| Rs. 2-5,00,000        | Defined-risk strategies (spreads). 1-3 lots.  |
| Rs. 5-15,00,000       | Mixed strategies. Allocate 60% to defined-risk.|
| Rs. 15-50,00,000      | Full strategy repertoire. Use portfolio margin.|
| > Rs. 50,00,000       | Multi-strategy portfolios. Diversify across underlyings.|

### Diversification Rules

- Do not allocate more than 30% of capital to a single underlying.
- Do not allocate more than 50% of capital to a single strategy type.
- Maintain at least 20% of capital as cash buffer for margin calls and adjustments.
- For undefined-risk positions, the margin requirement itself limits position size.

### Scaling Positions

- Start with 1 lot. Add lots only after the position moves in your favor.
- Never average down on a losing options position (especially for buyers).
- For sellers, consider adding lots at different strikes (laddering) rather
  than doubling at the same strike.

---

## 12. Rollover Strategies Near Expiry

### What is Rollover?

Rollover is the process of closing a position in the expiring contract and
simultaneously opening the same (or similar) position in the next expiry
contract. This allows traders to maintain their market exposure without physical
settlement or contract expiry.

### When to Roll

| Scenario                        | Action                                    |
|---------------------------------|-------------------------------------------|
| Profitable position, view intact | Roll to next expiry to extend duration    |
| Losing position, view still valid| Roll and adjust (different strike/strategy)|
| At-the-money near expiry        | Roll to avoid gamma risk and STT on exercise|
| Deep OTM with no value          | Let expire worthless (no need to roll)     |
| Deep ITM near expiry (stocks)   | Roll to avoid physical settlement          |

### Rollover Mechanics

#### For Index Options (Cash Settled)

1. Close the current expiry position.
2. Open the equivalent position in the next expiry.
3. The difference in premium between the two expiries is the rollover cost
   (debit) or credit.

#### For Stock Options (Physically Settled)

1. Must close before expiry to avoid physical delivery and associated margins.
2. Stock ITM options at expiry trigger physical settlement, requiring full
   delivery margin (entire stock value x lot size).
3. Close at least 2-3 days before expiry to avoid margin issues.

### Rollover Cost Analysis

The rollover cost depends on:

- **Time value of the new contract:** More time = more expensive.
- **Changes in implied volatility:** If IV has risen, the new contract is
  more expensive; if IV has fallen, it may be cheaper.
- **Interest rate component:** Far-month contracts embed higher carry cost.
- **Dividends:** Expected dividends reduce call premiums and increase put
  premiums in the far-month contract.

### Roll Strategies

#### 1. Straight Roll (Same Strike, Next Expiry)

- Close current month position.
- Open same strike, same type in next month.
- Simplest but may not be optimal if the underlying has moved significantly.

#### 2. Roll and Adjust (Different Strike)

- Close current position.
- Open at a different strike in next month that better reflects the current
  market conditions and your updated view.
- Example: If you sold NIFTY 24500 CE and NIFTY has risen to 24400, roll to
  selling NIFTY 25000 CE in the next month.

#### 3. Roll Up / Roll Down

- **Roll Up (for calls):** Close lower-strike call, open higher-strike call.
  Used when the underlying has moved up and you want to capture more upside
  in a covered call strategy.
- **Roll Down (for puts):** Close higher-strike put, open lower-strike put.
  Used when the underlying has fallen and you want to adjust your support level.

#### 4. Roll and Widen (for Spreads)

- Close the current spread.
- Open a wider spread in the next month.
- Captures more premium but increases maximum risk.

### Rollover Timing

- **Ideal rollover window:** 3-5 days before expiry for monthly contracts;
  1-2 days for weekly contracts.
- **Liquidity consideration:** Rollover too close to expiry results in wide
  bid-ask spreads in the expiring contract. Rollover too early means you
  miss out on theta decay in the current contract.
- **Cost consideration:** The rollover cost (net debit/credit) should be
  factored into the overall strategy P/L.

### Rollover Ratio (Market Indicator)

The rollover ratio for Nifty and Bank Nifty futures is a widely watched
market indicator:

- **High rollover (> 75%):** Strong conviction; traders are carrying positions
  forward. Bullish if long rollover, bearish if short rollover.
- **Low rollover (< 60%):** Lack of conviction. Traders are squaring off
  rather than rolling forward. Can signal a trend change.
- **Rollover with basis:** If the basis (futures premium over spot) increases
  during rollover, it signals bullish sentiment. If the basis decreases
  (or becomes negative/backwardation), it signals bearish sentiment.

---

## Appendix: Quick Reference Formulas

### Black-Scholes (European Options)

```
d1 = [ln(S/K) + (r - q + sigma^2/2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)

Call = S * exp(-q*T) * N(d1) - K * exp(-r*T) * N(d2)
Put  = K * exp(-r*T) * N(-d2) - S * exp(-q*T) * N(-d1)
```

Where:
- S = Spot price
- K = Strike price
- T = Time to expiry (in years)
- r = Risk-free rate (India 91-day T-bill, ~6.5-7%)
- q = Dividend yield
- sigma = Annualized volatility
- N() = Cumulative standard normal distribution

### Greeks

| Greek | Call                              | Put                                |
|-------|-----------------------------------|------------------------------------|
| Delta | exp(-qT) * N(d1)                | exp(-qT) * [N(d1) - 1]           |
| Gamma | exp(-qT) * n(d1) / (S*sigma*sqrt(T)) | Same as Call              |
| Theta | -(S*exp(-qT)*n(d1)*sigma)/(2*sqrt(T)) - r*K*exp(-rT)*N(d2) + q*S*exp(-qT)*N(d1) | -(S*exp(-qT)*n(d1)*sigma)/(2*sqrt(T)) + r*K*exp(-rT)*N(-d2) - q*S*exp(-qT)*N(-d1) |
| Vega  | S * exp(-qT) * n(d1) * sqrt(T)  | Same as Call                       |
| Rho   | K * T * exp(-rT) * N(d2)        | -K * T * exp(-rT) * N(-d2)        |

Where n() = standard normal PDF.

### Put-Call Parity (European)

```
Call - Put = S * exp(-q*T) - K * exp(-r*T)
```

### Expected Daily Move

```
Expected move = Spot * (India VIX / 100) / sqrt(252)
```

### Position Greeks (Multi-Leg)

```
Net Delta = Sum of (Direction_i * Delta_i * Lots_i * LotSize_i)
Net Gamma = Sum of (Direction_i * Gamma_i * Lots_i * LotSize_i)
Net Theta = Sum of (Direction_i * Theta_i * Lots_i * LotSize_i)
Net Vega  = Sum of (Direction_i * Vega_i  * Lots_i * LotSize_i)
```

Where Direction = +1 for long, -1 for short.
