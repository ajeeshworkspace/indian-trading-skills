# Financial Metrics Reference for Indian Stock Analysis

This reference document contains all key financial ratios, formulas, interpretation guidelines, and benchmarks for analyzing Indian listed companies. All metrics are organized by category for quick lookup during analysis.

---

## 1. Profitability Ratios

### Return on Equity (ROE)

- **Formula:** Net Profit / Average Shareholder's Equity x 100
- **What it measures:** How efficiently a company uses shareholder capital to generate profits.
- **Benchmark:** >15% is good, >20% is excellent for Indian companies.
- **Caution:** High ROE driven purely by leverage (high Debt/Equity) is less sustainable. Use DuPont analysis to decompose.
- **DuPont Decomposition:** ROE = Net Margin x Asset Turnover x Equity Multiplier
  - Net Margin = Net Profit / Revenue (profitability)
  - Asset Turnover = Revenue / Total Assets (efficiency)
  - Equity Multiplier = Total Assets / Equity (leverage)

### Return on Assets (ROA)

- **Formula:** Net Profit / Average Total Assets x 100
- **What it measures:** How efficiently a company uses all its assets (debt + equity funded) to generate profits.
- **Benchmark:** >5% for non-financial companies, >1% for banks.
- **Use case:** Better than ROE for comparing companies with different capital structures.

### Return on Capital Employed (ROCE)

- **Formula:** EBIT / (Total Assets - Current Liabilities) x 100
- **What it measures:** Returns generated on long-term capital (equity + long-term debt).
- **Benchmark:** >15% is good, should be higher than cost of debt.
- **India note:** ROCE is widely used by Indian analysts and is often more relevant than ROE for capital-intensive businesses.

### Return on Invested Capital (ROIC)

- **Formula:** NOPAT / Invested Capital x 100
  - NOPAT = Operating Profit x (1 - Tax Rate)
  - Invested Capital = Total Equity + Total Debt - Cash and Cash Equivalents
- **What it measures:** The true return on all invested capital, independent of capital structure.
- **Benchmark:** Should exceed the company's WACC (typically 10-14% in India).
- **Key insight:** ROIC > WACC means the company creates value; ROIC < WACC means it destroys value.

### Operating Profit Margin (OPM)

- **Formula:** Operating Profit / Revenue x 100
- **What it measures:** Profitability from core operations before interest and taxes.
- **Sector benchmarks for India:**

| Sector | Typical OPM Range |
|--------|-------------------|
| IT Services | 20-28% |
| FMCG | 18-25% |
| Pharmaceuticals | 18-25% |
| Automobiles | 10-15% |
| Banks (NIM as proxy) | 3-4% |
| Cement | 15-22% |
| Steel/Metals | 10-20% (cyclical) |
| Real Estate | 25-40% |
| Telecom | 30-50% |
| Retail | 3-8% |

### Net Profit Margin (NPM)

- **Formula:** Net Profit / Revenue x 100
- **What it measures:** Bottom-line profitability after all expenses, interest, and taxes.
- **Interpretation:** Compare with OPM to understand the impact of interest costs and taxes. A large gap between OPM and NPM suggests high leverage or high effective tax rate.

### EBITDA Margin

- **Formula:** (Revenue - Operating Expenses + Depreciation + Amortization) / Revenue x 100
  - Alternatively: EBITDA / Revenue x 100
- **What it measures:** Operating profitability before non-cash charges and capital structure effects.
- **Use case:** Best for comparing companies with different depreciation policies or asset ages. Widely used in Indian M&A valuations.

---

## 2. Valuation Ratios

### Price to Earnings Ratio (PE)

- **Formula:** Market Price per Share / Earnings per Share (EPS)
- **Variants:**
  - Trailing PE: Based on last 12 months (TTM) reported earnings
  - Forward PE: Based on estimated next 12 months earnings
- **Indian market context:**
  - Nifty 50 long-term average PE: approximately 20-22x
  - Large-cap range: 15-30x (sector dependent)
  - Mid-cap range: 18-40x
  - Small-cap range: 12-50x (high dispersion)
- **Compare with:** Industry PE (available from Groww data), sector PE, own historical PE range.
- **Limitation:** Not useful for loss-making companies or cyclical businesses at earnings peaks/troughs.

### Price to Book Ratio (PB)

- **Formula:** Market Price per Share / Book Value per Share
  - Book Value per Share = (Total Equity - Preference Share Capital) / Number of Equity Shares
- **Benchmark:**
  - PB < 1: Trading below book value (could be a value trap or genuine undervaluation)
  - PB 1-3: Reasonable for most sectors
  - PB > 5: Justified only for high-ROE businesses (ROE > 20%)
- **Key relationship:** PB = PE x ROE. A stock with PB of 5 and ROE of 25% has an implied PE of 20x.
- **Best for:** Banks, NBFCs, asset-heavy companies.

### Enterprise Value to EBITDA (EV/EBITDA)

- **Formula:**
  - Enterprise Value = Market Cap + Total Debt - Cash and Cash Equivalents
  - EV/EBITDA = Enterprise Value / EBITDA
- **Benchmark:**
  - <8x: Potentially undervalued (or low growth)
  - 8-15x: Fair value range for most sectors
  - 15-25x: Premium valuation (needs high growth)
  - >25x: Expensive (needs exceptional growth or asset value)
- **Advantage:** Capital structure neutral; better than PE for comparing companies with different leverage.

### PEG Ratio (Price/Earnings to Growth)

- **Formula:** PE Ratio / EPS Growth Rate (%)
  - Use 3-year EPS CAGR for growth rate
- **Interpretation:**
  - PEG < 0.5: Potentially significantly undervalued relative to growth
  - PEG 0.5-1.0: Attractively valued relative to growth
  - PEG 1.0-1.5: Fairly valued
  - PEG 1.5-2.0: Getting expensive
  - PEG > 2.0: Expensive relative to growth
- **Caution:** Growth rates should be sustainable; do not use abnormal one-year spikes.

### Price to Sales Ratio (P/S)

- **Formula:** Market Cap / Total Revenue (or Market Price per Share / Revenue per Share)
- **Use case:** Useful for loss-making companies, early-stage companies, or companies with depressed margins.
- **Benchmark:** Highly sector dependent. IT services: 3-6x; FMCG: 5-10x; Commodities: 0.5-2x.

### Earnings Yield

- **Formula:** EPS / Market Price per Share x 100 (i.e., 1/PE x 100)
- **Use case:** Compare with risk-free rate (India 10-year G-Sec yield, typically 6.5-7.5%).
- **Interpretation:** If earnings yield is below the G-Sec yield, the stock is expensive on an absolute basis and needs very high growth to justify the valuation.

### Dividend Yield

- **Formula:** Annual Dividend per Share / Market Price per Share x 100
- **Indian tax context:** Dividends are taxed in the hands of the shareholder at their income tax slab rate (post-2020 Finance Act).
- **Benchmark:** Compare with bank FD rates (6-7%). Dividend yield > FD rate with growth = attractive for income investors.
- **High-yield Indian sectors:** Coal India, Power Grid, IOC, BPCL, Vedanta, ITC (historically).

---

## 3. Growth Metrics

### Revenue Growth (CAGR)

- **Formula:** ((Revenue_End / Revenue_Start) ^ (1/n) - 1) x 100
  - Where n = number of years
- **Benchmark:**
  - >20% CAGR over 5 years: High growth
  - 10-20% CAGR: Moderate growth
  - 5-10% CAGR: Stable/low growth
  - <5% CAGR: Stagnant
- **India context:** Nominal GDP growth of 10-12% is a baseline. Companies growing below nominal GDP are losing real market share.

### EPS Growth

- **Formula:** ((EPS_End / EPS_Start) ^ (1/n) - 1) x 100
- **Comparison:** EPS growth should ideally be higher than revenue growth (indicating margin expansion or operating leverage).
- **Watch for:** EPS growth driven by buybacks (reducing share count) rather than genuine profit growth.

### Profit After Tax (PAT) Growth

- **Formula:** ((PAT_End / PAT_Start) ^ (1/n) - 1) x 100
- **Preferred over EPS growth** when share count has changed significantly due to stock splits, bonuses, or dilution.

### Book Value Growth

- **Formula:** ((Book Value_End / Book Value_Start) ^ (1/n) - 1) x 100
- **Significance:** Compounding book value at a high rate is a hallmark of long-term wealth creators. Warren Buffett's key metric.
- **Target:** > 15% CAGR in book value over 10 years indicates a quality compounder.

---

## 4. Leverage and Solvency Ratios

### Debt to Equity Ratio (D/E)

- **Formula:** Total Debt / Total Shareholder's Equity
- **Benchmark by sector:**

| Sector | Comfortable D/E | Caution | Red Flag |
|--------|-----------------|---------|----------|
| IT Services | 0-0.2 | 0.2-0.5 | >0.5 |
| FMCG | 0-0.3 | 0.3-0.7 | >0.7 |
| Pharmaceuticals | 0-0.5 | 0.5-1.0 | >1.0 |
| Automobiles | 0-0.5 | 0.5-1.0 | >1.0 |
| Infrastructure/Real Estate | 0.5-1.0 | 1.0-2.0 | >2.0 |
| Banks/NBFCs | Not applicable (use CAR) | -- | -- |
| Utilities | 0.5-1.5 | 1.5-2.5 | >2.5 |

### Interest Coverage Ratio (ICR)

- **Formula:** EBIT / Interest Expense
- **Interpretation:**
  - >6x: Very comfortable
  - 4-6x: Comfortable
  - 2-4x: Adequate but monitor
  - 1-2x: Strained; risk of default if business deteriorates
  - <1x: Cannot cover interest from operations; very high risk

### Current Ratio

- **Formula:** Current Assets / Current Liabilities
- **Benchmark:** >1.5 is healthy, <1.0 indicates potential liquidity stress.
- **India context:** Very low current ratios are common in trading companies and NBFCs where the business model involves short-term borrowing.

### Quick Ratio (Acid Test)

- **Formula:** (Current Assets - Inventory) / Current Liabilities
- **Benchmark:** >1.0 indicates the company can meet short-term obligations without selling inventory.
- **Use case:** More conservative than current ratio; especially relevant for companies with slow-moving inventory.

### Cash Ratio

- **Formula:** (Cash + Cash Equivalents) / Current Liabilities
- **Benchmark:** >0.2 indicates adequate cash buffer.
- **Use case:** Most conservative liquidity measure.

### Debt to Asset Ratio

- **Formula:** Total Debt / Total Assets
- **Benchmark:** <0.3 is conservative, 0.3-0.5 is moderate, >0.5 is aggressive.

---

## 5. Efficiency Ratios

### Asset Turnover Ratio

- **Formula:** Revenue / Average Total Assets
- **What it measures:** How efficiently the company uses its assets to generate revenue.
- **Interpretation:** Higher is better. Asset-light businesses (IT, FMCG) have high turnover; asset-heavy businesses (steel, power) have low turnover.
- **DuPont link:** Higher asset turnover can compensate for lower margins in generating ROE.

### Inventory Turnover Ratio

- **Formula:** Cost of Goods Sold / Average Inventory
- **Interpretation:** Higher is better (faster inventory conversion). Very low turnover may indicate obsolete stock.
- **Sector context:** FMCG and retail should have high turnover; capital goods and real estate will have low turnover.

### Inventory Days

- **Formula:** 365 / Inventory Turnover
- **Interpretation:** Fewer days is better. Increasing inventory days can signal slowing demand.

### Receivable Turnover Ratio

- **Formula:** Revenue / Average Trade Receivables
- **Interpretation:** Higher is better (faster collection).

### Receivable Days (Days Sales Outstanding)

- **Formula:** 365 / Receivable Turnover (or Average Receivables / Revenue x 365)
- **Interpretation:** Fewer days is better. Increasing receivable days can signal:
  - Channel stuffing (pushing inventory to dealers/distributors)
  - Deteriorating collection efficiency
  - Customer financial stress
- **India context:** Government and PSU receivables in India can have very long payment cycles (90-180 days is not uncommon for infrastructure companies).

### Payable Days

- **Formula:** Average Trade Payables / Cost of Goods Sold x 365
- **Interpretation:** Higher payable days indicate better bargaining power with suppliers but can also signal financial stress if increasing sharply.

### Cash Conversion Cycle (CCC)

- **Formula:** Inventory Days + Receivable Days - Payable Days
- **Interpretation:**
  - Negative CCC: Excellent (company gets paid before it pays suppliers, e.g., some FMCG companies)
  - 0-30 days: Very efficient
  - 30-90 days: Normal for most manufacturing
  - >90 days: Capital-intensive or inefficient working capital management

---

## 6. Cash Flow Metrics

### Free Cash Flow (FCF)

- **Formula:** Operating Cash Flow - Capital Expenditure
- **Interpretation:** Positive and growing FCF is a strong sign. Negative FCF is acceptable only during heavy capex phases for growth-stage companies.
- **Quality check:** FCF yield (FCF / Market Cap) above 4-5% is attractive for mature businesses.

### Operating Cash Flow to PAT Ratio (OCF/PAT)

- **Formula:** Operating Cash Flow / Profit After Tax
- **Benchmark:**
  - >1.0: Excellent cash conversion (cash earnings exceed accounting earnings)
  - 0.8-1.0: Good
  - 0.5-0.8: Moderate; investigate accruals and working capital
  - <0.5: Poor; earnings quality is questionable
- **Why this matters:** Indian companies sometimes show accounting profits that do not translate into cash. This ratio exposes that gap.

### Capex to Revenue Ratio

- **Formula:** Capital Expenditure / Revenue x 100
- **Interpretation:**
  - <5%: Asset-light business (IT, consulting)
  - 5-10%: Moderate capex (FMCG, pharma)
  - 10-20%: Capital-intensive (automobiles, cement)
  - >20%: Very capital-intensive (steel, power, telecom) or heavy expansion phase

### Capex to Depreciation Ratio

- **Formula:** Capital Expenditure / Depreciation
- **Interpretation:**
  - >1.5: Investing for growth (expanding asset base)
  - 1.0-1.5: Maintaining asset base
  - <1.0: Under-investing; may face future capacity issues

### Free Cash Flow Yield

- **Formula:** Free Cash Flow / Market Cap x 100
- **Benchmark:**
  - >5%: Attractive for mature businesses
  - 3-5%: Fair
  - <3%: Expensive on cash flow basis (needs high growth justification)

---

## 7. India-Specific Ownership Metrics

### Promoter Holding Percentage

- **Formula:** Shares held by Promoters and Promoter Group / Total Shares Outstanding x 100
- **Data source:** Quarterly shareholding pattern filed with BSE/NSE under SEBI LODR regulations. Available via Groww MCP `fetch_stocks_fundamental_data` with `view='shareholding_only'`.
- **Assessment guide:**

| Range | Rating | Interpretation |
|-------|--------|---------------|
| >70% | Neutral to Positive | High control but low free float; check for governance |
| 50-70% | Positive | Strong promoter confidence with adequate free float |
| 35-50% | Neutral | Moderate holding; watch trends |
| 20-35% | Caution | Low holding; governance and hostile takeover risk |
| <20% | Evaluate | Could be professional management (Infosys, HDFC Bank) or weak promoter |

### Promoter Pledge Percentage

- **Formula:** Shares Pledged by Promoters / Total Promoter Holding x 100
- **Data source:** Quarterly shareholding pattern disclosures.
- **Assessment guide:**

| Range | Risk Level | Action |
|-------|-----------|--------|
| 0% | No Risk | Ideal scenario |
| 1-10% | Low Risk | Monitor quarterly |
| 10-20% | Moderate Risk | Investigate reason; stronger fundamentals needed |
| 20-40% | High Risk | Red flag; consider reducing exposure |
| >40% | Very High Risk | Avoid unless exceptional circumstances |

### FII Holding Percentage

- **Formula:** Shares held by Foreign Institutional Investors / Total Shares Outstanding x 100
- **Interpretation:**
  - >30%: High FII ownership; stock is sensitive to global risk sentiment and INR/USD
  - 15-30%: Well-discovered by foreign investors
  - 5-15%: Moderate foreign interest
  - <5%: Under-discovered by FIIs or structural concerns

### DII Holding Percentage

- **Formula:** Shares held by Domestic Institutional Investors / Total Shares Outstanding x 100
- **Components:** Mutual funds, insurance companies (LIC), pension funds (EPFO), banks.
- **Significance:** DII flows have become increasingly important due to the growth of SIP-based mutual fund investing in India.

### Public/Retail Holding Percentage

- **Formula:** 100% - Promoter% - FII% - DII%
- **Interpretation:**
  - Very high retail holding (>50%) can indicate speculative interest
  - Increasing retail holding while FII/DII reduce often signals distribution by smart money

---

## 8. Banking-Specific Metrics

These metrics apply specifically to banks and NBFCs, which are analyzed differently from non-financial companies.

### Net Interest Margin (NIM)

- **Formula:** (Interest Income - Interest Expense) / Average Interest-Earning Assets x 100
- **Benchmark:** >3.5% for private banks, >2.5% for PSU banks.

### Gross NPA Ratio

- **Formula:** Gross Non-Performing Assets / Gross Advances x 100
- **Benchmark:** <2% is excellent, 2-5% is acceptable, >5% is concerning.

### Net NPA Ratio

- **Formula:** Net NPAs / Net Advances x 100
- **Benchmark:** <1% is excellent, 1-2% is acceptable, >3% is a red flag.

### CASA Ratio

- **Formula:** (Current Account Deposits + Savings Account Deposits) / Total Deposits x 100
- **Benchmark:** >40% is strong (indicates low cost of funds).

### Provision Coverage Ratio (PCR)

- **Formula:** Cumulative Provisions / Gross NPAs x 100
- **Benchmark:** >70% is comfortable.

### Credit Cost

- **Formula:** Loan Loss Provisions / Average Advances x 100
- **Benchmark:** <1% is healthy for most cycles.

### Slippage Ratio

- **Formula:** Fresh NPAs during the period / Standard Advances at the beginning x 100
- **Benchmark:** <2% annualized is acceptable.

---

## 9. Metric Interpretation Summary Table

Quick reference for evaluating any Indian stock:

| Metric | Excellent | Good | Average | Poor | Red Flag |
|--------|-----------|------|---------|------|----------|
| ROE | >20% | 15-20% | 10-15% | 5-10% | <5% |
| ROCE | >20% | 15-20% | 10-15% | 5-10% | <5% |
| OPM | >25% | 15-25% | 10-15% | 5-10% | <5% |
| Debt/Equity | <0.2 | 0.2-0.5 | 0.5-1.0 | 1.0-2.0 | >2.0 |
| Interest Coverage | >6x | 4-6x | 2-4x | 1-2x | <1x |
| Current Ratio | >2.0 | 1.5-2.0 | 1.0-1.5 | 0.7-1.0 | <0.7 |
| OCF/PAT | >1.2 | 0.8-1.2 | 0.5-0.8 | 0.2-0.5 | <0.2 |
| Promoter Holding | >60% | 50-60% | 35-50% | 20-35% | <20% |
| Promoter Pledge | 0% | 1-10% | 10-20% | 20-40% | >40% |
| PE vs Industry PE | >20% discount | 0-20% discount | At par | 0-20% premium | >20% premium |
| PEG Ratio | <0.5 | 0.5-1.0 | 1.0-1.5 | 1.5-2.0 | >2.0 |
| FCF Yield | >6% | 4-6% | 2-4% | 0-2% | Negative |
| Dividend Yield | >4% | 2-4% | 1-2% | 0.5-1% | 0% (no dividend) |
| Revenue CAGR (5Y) | >20% | 12-20% | 8-12% | 3-8% | <3% |
| EPS CAGR (5Y) | >25% | 15-25% | 8-15% | 0-8% | Negative |

---

## 10. Formulas Quick Reference

A compact reference for all formulas:

```
PROFITABILITY
  ROE              = Net Profit / Avg Shareholder Equity x 100
  ROA              = Net Profit / Avg Total Assets x 100
  ROCE             = EBIT / (Total Assets - Current Liabilities) x 100
  ROIC             = NOPAT / Invested Capital x 100
  Operating Margin = Operating Profit / Revenue x 100
  Net Margin       = Net Profit / Revenue x 100
  EBITDA Margin    = EBITDA / Revenue x 100

VALUATION
  PE               = Market Price / EPS
  PB               = Market Price / Book Value per Share
  EV/EBITDA        = (Market Cap + Debt - Cash) / EBITDA
  PEG              = PE / EPS Growth Rate
  P/S              = Market Cap / Revenue
  Earnings Yield   = EPS / Market Price x 100  (or 1/PE x 100)
  Dividend Yield   = DPS / Market Price x 100

GROWTH
  Revenue CAGR     = (Revenue_End / Revenue_Start) ^ (1/n) - 1
  EPS CAGR         = (EPS_End / EPS_Start) ^ (1/n) - 1
  Book Value CAGR  = (BV_End / BV_Start) ^ (1/n) - 1

LEVERAGE
  Debt/Equity      = Total Debt / Total Equity
  Interest Cover   = EBIT / Interest Expense
  Current Ratio    = Current Assets / Current Liabilities
  Quick Ratio      = (Current Assets - Inventory) / Current Liabilities
  Cash Ratio       = Cash / Current Liabilities
  Debt/Asset       = Total Debt / Total Assets
  Net Debt/EBITDA  = (Total Debt - Cash) / EBITDA

EFFICIENCY
  Asset Turnover   = Revenue / Avg Total Assets
  Inventory Turn   = COGS / Avg Inventory
  Inventory Days   = 365 / Inventory Turnover
  Receivable Days  = Avg Receivables / Revenue x 365
  Payable Days     = Avg Payables / COGS x 365
  Cash Conv Cycle  = Inv Days + Recv Days - Pay Days

CASH FLOW
  FCF              = Operating Cash Flow - Capex
  OCF/PAT          = Operating Cash Flow / Profit After Tax
  Capex/Revenue    = Capital Expenditure / Revenue x 100
  Capex/Deprn      = Capital Expenditure / Depreciation
  FCF Yield        = FCF / Market Cap x 100

OWNERSHIP (INDIA)
  Promoter %       = Promoter Shares / Total Shares x 100
  Pledge %         = Pledged Shares / Promoter Shares x 100
  FII %            = FII Shares / Total Shares x 100
  DII %            = DII Shares / Total Shares x 100
  Public %         = 100 - Promoter% - FII% - DII%
```
