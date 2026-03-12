# Sector Sensitivity Matrix — Indian Markets

Maps event types to their impact on NSE sectoral indices. Impact rated as: **High** (H), **Medium** (M), **Low** (L), **Positive** (+) or **Negative** (-).

## Event × Sector Impact Matrix

| Event | Banks | IT | Pharma | Auto | FMCG | Metal | Realty | Energy | Infra | Telecom |
|-------|-------|-----|--------|------|------|-------|--------|--------|-------|---------|
| RBI Rate Cut | H+ | L | L | H+ | M+ | L | H+ | L | M+ | L |
| RBI Rate Hike | H- | L | L | M- | L | L | H- | L | M- | L |
| INR Depreciation | M- | H+ | H+ | M- | L | M- | L | M- | L | L |
| INR Appreciation | M+ | H- | H- | M+ | L | M+ | L | M+ | L | L |
| Crude Up | L | L | L | M- | L | L | L | H+/- | L | L |
| Crude Down | L | L | L | M+ | L | L | L | H-/+ | L | L |
| US Recession | M- | H- | M+ | M- | M+ | H- | M- | M- | M- | L |
| Global Growth | M+ | H+ | L | M+ | L | H+ | M+ | M+ | M+ | L |
| Budget Capex | L | L | L | L | L | M+ | M+ | L | H+ | L |
| Income Tax Cut | M+ | L | L | M+ | H+ | L | M+ | L | L | L |
| Monsoon (Good) | M+ | L | L | M+ | H+ | L | L | L | L | L |
| Monsoon (Poor) | M- | L | L | L | M- | L | L | L | L | L |
| FII Outflows | H- | M- | M- | M- | L | M- | M- | M- | M- | L |
| FII Inflows | H+ | M+ | L | M+ | L | M+ | M+ | M+ | M+ | L |
| China Slowdown | L | L | L | L | L | H- | L | M- | L | L |
| Food Inflation | M- | L | L | L | M- | L | L | L | L | L |
| Defense Spending | L | L | L | L | L | L | L | L | M+ | L |

## Sector Profiles

### Nifty Bank (Weight: ~33% of Nifty 50)
- **Primary drivers**: Interest rates, credit growth, asset quality (NPA)
- **Most sensitive to**: RBI policy, global liquidity, FII flows
- **Sub-sectors**: Private banks (HDFC, ICICI, Kotak), PSU banks (SBI, BOB, PNB), NBFCs (Bajaj Finance)

### Nifty IT (Weight: ~14%)
- **Primary drivers**: USD/INR, US tech spending, deal wins
- **Most sensitive to**: INR movement, US economic outlook, visa policies
- **Inverse correlation**: Often moves opposite to banking/rate-sensitive sectors

### Nifty Pharma (Weight: ~4%)
- **Primary drivers**: US FDA approvals, ANDA pipeline, domestic formulations
- **Most sensitive to**: USD/INR (exports), FDA regulatory actions
- **Defensive**: Outperforms during risk-off, underperforms in strong bull markets

### Nifty Auto (Weight: ~6%)
- **Primary drivers**: Interest rates, fuel prices, monsoon (rural demand), EV transition
- **Most sensitive to**: Consumer sentiment, commodity prices (steel input cost)
- **Sub-segments**: Passenger vehicles (Maruti, M&M), Two-wheelers (Hero, Bajaj), Commercial vehicles (Tata Motors, Ashok Leyland)

### Nifty FMCG (Weight: ~8%)
- **Primary drivers**: Rural demand, monsoon, raw material costs
- **Most sensitive to**: Consumer inflation, monsoon, income tax changes
- **Defensive**: Low beta, steady in corrections, underperforms in strong rallies

### Nifty Metal (Weight: ~3%)
- **Primary drivers**: Global commodity prices, China demand, US infrastructure
- **Most sensitive to**: China PMI, global trade tensions, USD strength
- **Cyclical**: High beta, large swings with commodity cycles

### Nifty Realty (Weight: ~2%)
- **Primary drivers**: Interest rates, regulatory (RERA), demand cycles
- **Most sensitive to**: RBI rate decisions, housing demand, liquidity
- **High beta**: Amplifies both up and down moves

### Nifty Energy (Weight: ~12%)
- **Primary drivers**: Crude oil prices, government subsidy policy, gas pricing
- **Complex**: Oil producers (ONGC, Oil India) benefit from high crude; OMCs (BPCL, HPCL) suffer
- **Key distinction**: Upstream (positive crude correlation) vs downstream (negative)

### Nifty Infrastructure (Weight: ~5%)
- **Primary drivers**: Government capex, budget allocation, order inflows
- **Most sensitive to**: Budget announcements, government spending pace
- **Key stocks**: L&T, Adani Ports, Ultratech Cement

## Using This Matrix

1. **Identify the event type** from the headline
2. **Look up the row** in the matrix for direct impact sectors
3. **Follow the cascade**: 1° impact → 2° impact → 3° impact
4. **Verify with historical patterns** from headline_event_patterns.md
5. **Consider timing**: Some impacts are immediate, others take months

### Example: "RBI Cuts Rate by 25 bps"

1° (Immediate): Banks (H+), Realty (H+), Auto (H+)
2° (1-3 months): NBFC (M+), Housing Finance (M+), Consumer Durables (M+)
3° (3-6 months): Cement (L+), Infrastructure (M+), FMCG rural (L+)
