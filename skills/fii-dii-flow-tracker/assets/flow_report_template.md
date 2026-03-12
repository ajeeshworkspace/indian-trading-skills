# FII/DII Flow Report Template

Use this template to generate standardized institutional flow analysis reports. Replace all placeholders (wrapped in curly braces) with actual data. Remove any sections that are not applicable.

---

## Report Output Begins Below

---

# Institutional Flow Analysis Report

**Report Date:** {report_date}
**Market Status:** {market_open_or_closed}
**Data Type:** {provisional_or_final}
**Nifty 50 Close:** {nifty_close} ({nifty_change_pct}%)

---

## 1. Flow Summary

### Today's Institutional Activity

| Category | Gross Buy (Cr) | Gross Sell (Cr) | Net (Cr) | Signal |
|----------|---------------|----------------|----------|--------|
| **FII/FPI** | {fii_gross_buy} | {fii_gross_sell} | **{fii_net}** | {fii_signal_emoji_text} |
| **DII** | {dii_gross_buy} | {dii_gross_sell} | **{dii_net}** | {dii_signal_emoji_text} |
| **Combined** | {combined_gross_buy} | {combined_gross_sell} | **{combined_net}** | {combined_signal_emoji_text} |

> **Signal Legend:** NET BUYER = Positive net inflow | NET SELLER = Negative net outflow | NEUTRAL = Absolute net below 500cr

### Period Aggregates

| Period | FII Net (Cr) | DII Net (Cr) | Combined Net (Cr) |
|--------|-------------|-------------|-------------------|
| Today | {fii_net_today} | {dii_net_today} | {combined_net_today} |
| Last 5 Days | {fii_net_5d} | {dii_net_5d} | {combined_net_5d} |
| MTD ({current_month}) | {fii_net_mtd} | {dii_net_mtd} | {combined_net_mtd} |
| Last Month ({previous_month}) | {fii_net_prev_month} | {dii_net_prev_month} | {combined_net_prev_month} |
| YTD ({current_year}) | {fii_net_ytd} | {dii_net_ytd} | {combined_net_ytd} |

---

## 2. Daily Flow Table (Last 10 Trading Days)

| Date | FII Net (Cr) | DII Net (Cr) | Combined Net (Cr) | Nifty Close | Nifty Chg (%) | Flow-Price Alignment |
|------|-------------|-------------|-------------------|-------------|---------------|---------------------|
| {date_1} | {fii_1} | {dii_1} | {combined_1} | {nifty_1} | {nifty_chg_1} | {alignment_1} |
| {date_2} | {fii_2} | {dii_2} | {combined_2} | {nifty_2} | {nifty_chg_2} | {alignment_2} |
| {date_3} | {fii_3} | {dii_3} | {combined_3} | {nifty_3} | {nifty_chg_3} | {alignment_3} |
| {date_4} | {fii_4} | {dii_4} | {combined_4} | {nifty_4} | {nifty_chg_4} | {alignment_4} |
| {date_5} | {fii_5} | {dii_5} | {combined_5} | {nifty_5} | {nifty_chg_5} | {alignment_5} |
| {date_6} | {fii_6} | {dii_6} | {combined_6} | {nifty_6} | {nifty_chg_6} | {alignment_6} |
| {date_7} | {fii_7} | {dii_7} | {combined_7} | {nifty_7} | {nifty_chg_7} | {alignment_7} |
| {date_8} | {fii_8} | {dii_8} | {combined_8} | {nifty_8} | {nifty_chg_8} | {alignment_8} |
| {date_9} | {fii_9} | {dii_9} | {combined_9} | {nifty_9} | {nifty_chg_9} | {alignment_9} |
| {date_10} | {fii_10} | {dii_10} | {combined_10} | {nifty_10} | {nifty_chg_10} | {alignment_10} |

> **Flow-Price Alignment** indicates whether FII net direction matched Nifty direction that day. "Aligned" means FII buying + Nifty up OR FII selling + Nifty down. "Divergent" means FII buying + Nifty down OR FII selling + Nifty up (suggests other forces dominating).

### 10-Day Summary Statistics

| Metric | FII | DII |
|--------|-----|-----|
| Net Buying Days | {fii_buy_days}/10 | {dii_buy_days}/10 |
| Net Selling Days | {fii_sell_days}/10 | {dii_sell_days}/10 |
| Largest Single-Day Buy | {fii_max_buy} ({fii_max_buy_date}) | {dii_max_buy} ({dii_max_buy_date}) |
| Largest Single-Day Sell | {fii_max_sell} ({fii_max_sell_date}) | {dii_max_sell} ({dii_max_sell_date}) |
| 10-Day Cumulative | {fii_10d_cumulative} | {dii_10d_cumulative} |
| Daily Average | {fii_daily_avg} | {dii_daily_avg} |

---

## 3. Trend Analysis

### FII Flow Trend

**Current Trend:** {fii_trend_direction} (Buying / Selling / Neutral)

**Trend Strength:** {fii_trend_strength} (Strong / Moderate / Weak)

**Trend Duration:** {fii_trend_duration} consecutive {buying_or_selling} days

**Acceleration/Deceleration:**
- Last 5 days average: {fii_avg_last_5d} cr/day
- Prior 5 days average: {fii_avg_prior_5d} cr/day
- Change: {fii_acceleration} (Accelerating if magnitude increasing, Decelerating if magnitude decreasing)

**Interpretation:** {fii_trend_interpretation}

> Example: "FII selling has been decelerating over the past week, with daily net selling declining from -3,500cr to -1,200cr. This deceleration suggests the current selling wave may be nearing exhaustion. If FII net crosses into positive territory in the next 2-3 days, it would signal a regime transition."

### DII Flow Trend

**Current Trend:** {dii_trend_direction} (Buying / Selling / Neutral)

**Trend Strength:** {dii_trend_strength} (Strong / Moderate / Weak)

**Trend Duration:** {dii_trend_duration} consecutive {buying_or_selling} days

**Interpretation:** {dii_trend_interpretation}

> Example: "DII have been consistent net buyers for the past 8 trading days, deploying an average of 2,100cr per day. This is above the baseline SIP-driven flow of approximately 1,200-1,500cr/day, indicating active deployment by mutual fund managers beyond SIP obligations. DII absorption rate of FII selling has averaged 72%."

### Monthly Comparison

| Month | FII Net (Cr) | DII Net (Cr) | Nifty Return |
|-------|-------------|-------------|--------------|
| {month_minus_3} | {fii_m3} | {dii_m3} | {nifty_ret_m3}% |
| {month_minus_2} | {fii_m2} | {dii_m2} | {nifty_ret_m2}% |
| {month_minus_1} | {fii_m1} | {dii_m1} | {nifty_ret_m1}% |
| {current_month} (MTD) | {fii_mtd} | {dii_mtd} | {nifty_ret_mtd}% |

**Monthly Trend Observation:** {monthly_trend_observation}

> Example: "FII selling has moderated significantly from -25,000cr in January to -8,000cr in February, and the current month is tracking at -3,000cr MTD. If this deceleration continues, March could see FII turning net positive. DII buying has been consistently above 15,000cr/month for the past 3 months, providing strong market support."

---

## 4. Nifty Correlation Analysis

### Flow-Price Correlation (Last 20 Trading Days)

| Metric | Value | Interpretation |
|--------|-------|----------------|
| FII Net vs Nifty Daily Change (same day) | {correlation_same_day} | {interpretation_same_day} |
| FII Net (t) vs Nifty Change (t+1) (predictive) | {correlation_predictive} | {interpretation_predictive} |
| FII 5-Day Sum vs Nifty 5-Day Return | {correlation_5d} | {interpretation_5d} |

> **Correlation Scale:** Above 0.7 = Strong, 0.4-0.7 = Moderate, Below 0.4 = Weak

### Flow-Price Alignment Score

Over the last 10 trading days, FII flow direction matched Nifty direction on **{alignment_days}/10 days** ({alignment_pct}%).

- **Above 70%:** FII flows are the dominant market driver currently.
- **50-70%:** FII flows are one of several factors influencing the market.
- **Below 50%:** Other factors (DII, retail, global cues, earnings) are more dominant than FII flows.

### Divergence Analysis

{divergence_analysis}

> Example: "Notable divergence observed on March 8 and March 9, where FII were net sellers (-1,800cr and -2,200cr respectively) but Nifty closed positive (+0.4% and +0.6%). This divergence was driven by strong DII buying (+2,500cr and +3,100cr) that more than offset FII outflow. DII buying power exceeded FII selling, indicating robust domestic demand at current levels."

---

## 5. Flow Regime Assessment

### Current Regime: **{current_regime}**

{regime_description}

> One of:
> - **FII Net Buyer Regime**: FII have been consistently net buyers. Market has a bullish bias from institutional flows. INR likely to be stable or strengthening.
> - **FII Net Seller Regime**: FII have been consistently net sellers. Market faces headwinds from foreign outflows. INR under depreciation pressure.
> - **DII Absorption Regime**: FII selling is being substantially absorbed by DII buying. Market is range-bound with a support floor from domestic flows.
> - **Dual Buying Regime**: Both FII and DII are net buyers. This is the most bullish institutional flow configuration. Strong rally potential.
> - **Dual Selling Regime**: Both FII and DII are net sellers. This is extremely rare and bearish. Sharp correction risk.
> - **Transition Phase**: Institutional flows are in the process of changing direction. Watch for confirmation over the next 3-5 trading days.

### Regime Details

| Metric | Value |
|--------|-------|
| Regime Start Date (approximate) | {regime_start_date} |
| Regime Duration | {regime_duration} trading days |
| FII Cumulative Since Regime Start | {fii_cumulative_regime} cr |
| DII Cumulative Since Regime Start | {dii_cumulative_regime} cr |
| DII Absorption Rate (if FII selling) | {absorption_rate}% |
| Nifty Change Since Regime Start | {nifty_change_regime}% |

### Regime Transition Watch

**Probability of Regime Change:** {regime_change_probability} (Low / Medium / High)

**Transition Signals:**
{transition_signals_list}

> Example:
> - FII selling magnitude has declined 40% over the last 5 days (deceleration signal)
> - FII posted one net buying day within the last 5 days (early reversal signal)
> - The catalyst for FII selling (US yield spike) has stabilized (fundamental driver fading)
> - FII index futures long/short ratio has improved from 0.45 to 0.62 (derivative positioning turning)
> - **Assessment: Medium probability of transition to FII Net Buyer Regime within 5-7 trading days**

---

## 6. Sector Impact Analysis

### Sector-Level Institutional Flow Indicators

| Sector | FII Positioning | DII Positioning | Net Institutional View | Key Stocks Affected |
|--------|----------------|-----------------|----------------------|-------------------|
| Banking/Financials | {banking_fii} | {banking_dii} | {banking_net} | {banking_stocks} |
| IT/Technology | {it_fii} | {it_dii} | {it_net} | {it_stocks} |
| FMCG/Consumer | {fmcg_fii} | {fmcg_dii} | {fmcg_net} | {fmcg_stocks} |
| Pharma/Healthcare | {pharma_fii} | {pharma_dii} | {pharma_net} | {pharma_stocks} |
| Automobile | {auto_fii} | {auto_dii} | {auto_net} | {auto_stocks} |
| Oil & Gas | {oil_fii} | {oil_dii} | {oil_net} | {oil_stocks} |
| Metals/Mining | {metals_fii} | {metals_dii} | {metals_net} | {metals_stocks} |
| Capital Goods/Infra | {capgoods_fii} | {capgoods_dii} | {capgoods_net} | {capgoods_stocks} |

> **Note:** Sector-level flow data is approximated from sectoral index performance, stock-level block deal activity, and quarterly shareholding changes. Daily sector-wise FII/DII data is not officially published; this assessment is based on available proxies.

### Sector Rotation Observations

{sector_rotation_observations}

> Example: "Over the past 2 weeks, banking stocks have underperformed the broader market by 2.3%, consistent with FII selling pressure on their largest sector holding. Conversely, IT stocks have outperformed by 1.8%, benefiting from both INR depreciation (driven by FII outflows) and relative valuation comfort. DII appear to be increasing allocation to Pharma and FMCG, based on mutual fund portfolio disclosures and sectoral index strength."

---

## 7. Market Implications

### Near-Term Outlook (1-2 Weeks)

**Institutional Flow Bias:** {near_term_bias} (Bullish / Bearish / Neutral)

**Confidence Level:** {near_term_confidence} (High / Medium / Low)

**Key Assessment:**

{near_term_assessment}

> Example: "The institutional flow environment currently favors a cautious-to-positive near-term outlook for Nifty. While FII remain net sellers, the deceleration in selling intensity combined with robust DII absorption (averaging 75%) suggests the worst of the selling pressure may be behind us. Combined institutional flow has been only mildly negative (-800cr/day average over the last 5 days), which is insufficient to drive significant further downside. If FII selling continues to moderate, Nifty can stabilize in the 22,500-23,000 range and potentially attempt a recovery toward 23,300-23,500."

### Medium-Term Outlook (1-3 Months)

**Institutional Flow Bias:** {medium_term_bias}

**Key Factors:**

1. {medium_term_factor_1}
2. {medium_term_factor_2}
3. {medium_term_factor_3}

{medium_term_assessment}

> Example:
> 1. FII YTD outflow of -45,000cr is significant but below the FY2022 pace (-1.4L cr FY total). If current monthly pace (-8,000cr/month) continues, full-year FII outflow would be approximately -96,000cr, manageable for the market.
> 2. DII buying capacity remains strong. SIP flows are stable at 25,000cr/month with no signs of slowing. Insurance and EPFO deployment continues on schedule.
> 3. The primary catalyst for FII selling (US Fed rate expectations) could shift in Q2 if US inflation data cooperates, which would reduce the pressure.
> Medium-term view: Cautiously positive. The DII floor limits downside to 5-7% from current levels, while FII selling moderation or reversal could trigger a 8-12% rally.

### Risk Scenarios

**Upside Risk (Bullish Scenario):**
{upside_scenario}

> Example: "If FII reverse to net buyers (triggered by a Fed dovish pivot or significant India GDP upgrade), Nifty could rally 8-12% from current levels within 2-3 months. Historical precedent: FII turning buyer in Q1 2024 preceded a 15% Nifty rally."

**Downside Risk (Bearish Scenario):**
{downside_scenario}

> Example: "If FII selling accelerates beyond 5,000cr/day (triggered by a global recession scare or India-specific shock), and DII absorption falls below 50%, Nifty could correct 8-12% from current levels. This would take Nifty toward the 20,500-21,000 zone."

---

## 8. Key Levels to Watch (In Context of Flows)

### Nifty Levels with Institutional Flow Context

| Level | Type | Flow Context |
|-------|------|-------------|
| {resistance_2} | Strong Resistance | {resistance_2_context} |
| {resistance_1} | Immediate Resistance | {resistance_1_context} |
| **{current_nifty}** | **Current Level** | **{current_context}** |
| {support_1} | Immediate Support | {support_1_context} |
| {support_2} | Strong Support | {support_2_context} |

> Example:
> | 23,500 | Strong Resistance | FII were last net buyers at this level; requires FII buying to sustain breakout above |
> | 23,000 | Immediate Resistance | Short-term supply zone; FII selling intensified on last test |
> | **22,650** | **Current Level** | **DII absorption providing floor; combined institutional flow mildly negative** |
> | 22,200 | Immediate Support | DII increased buying on last dip to this level; SIP-driven floor |
> | 21,800 | Strong Support | Major DII buying zone during previous correction; FII selling exhausted here last time |

### Critical Flow Thresholds

- **FII daily net needed for Nifty to sustain above {resistance_1}:** At least {fii_needed_for_breakout} cr/day net buying
- **DII daily net needed to hold {support_1}:** At least {dii_needed_for_support} cr/day net buying (if FII selling continues at current pace)
- **Combined institutional flow needed for trend reversal:** At least {combined_needed_for_reversal} cr/day for 5+ consecutive days

---

## 9. FII Derivative Position Summary (Supplementary)

| Metric | Current Value | Previous Day | Change | Signal |
|--------|-------------|-------------|--------|--------|
| FII Index Futures Long Contracts | {fii_fut_long} | {fii_fut_long_prev} | {fii_fut_long_chg} | {fii_fut_long_signal} |
| FII Index Futures Short Contracts | {fii_fut_short} | {fii_fut_short_prev} | {fii_fut_short_chg} | {fii_fut_short_signal} |
| FII Index Futures Net | {fii_fut_net} | {fii_fut_net_prev} | {fii_fut_net_chg} | {fii_fut_net_signal} |
| FII Long/Short Ratio | {fii_ls_ratio} | {fii_ls_ratio_prev} | {fii_ls_ratio_chg} | {fii_ls_ratio_signal} |
| FII Index Options Net (Calls) | {fii_opt_calls_net} | {fii_opt_calls_prev} | {fii_opt_calls_chg} | - |
| FII Index Options Net (Puts) | {fii_opt_puts_net} | {fii_opt_puts_prev} | {fii_opt_puts_chg} | - |

**Derivative Positioning Interpretation:** {derivative_interpretation}

> Example: "FII index futures long/short ratio has improved from 0.52 to 0.61 over the past 5 days, indicating gradual short-covering and long addition. While still net short (below 1.0), the trend is positive. FII have also been writing puts at 22,000-22,200 strikes, suggesting they do not expect Nifty to fall below these levels. Combined cash + derivative positioning is turning less bearish."

---

## 10. Disclaimer

**Important:** This report is for informational and educational purposes only. It does not constitute investment advice, a recommendation to buy or sell securities, or an offer of any financial product.

**Data Limitations:**
- FII/DII data reported here is based on publicly available sources (NSE, NSDL, MoneyControl). Minor discrepancies may exist between sources.
- Provisional data (if used) may differ from final data by 2-5%.
- Daily aggregate FII/DII data does not reveal stock-level or sector-level flows. Sector assessments in this report are based on proxies and should be treated as indicative, not definitive.
- Derivative position data is based on NSE participant-wise open interest reports and reflects positions at end of day.

**Analytical Limitations:**
- Institutional flow analysis is one input among many for market assessment. It should not be used in isolation.
- Historical patterns and correlations may not repeat in the future.
- Flow data is backward-looking (what happened) and has limited predictive power for future flows.
- Single-day data is inherently noisy. Trends identified over 5-10 day periods are more reliable than daily readings.

**Risk Warning:**
- Equity investments are subject to market risk. Past institutional flow patterns do not guarantee future market performance.
- FII flows can reverse rapidly and without warning based on global events.
- The correlation between institutional flows and market direction varies over time and can break down during unusual market conditions.

**This report was generated on {report_date} at {report_time} IST. Data reflects the most recent available information at the time of generation.**

---

*Report generated using the FII/DII Flow Tracker skill. Data sourced from NSE, NSDL, and market data providers.*
