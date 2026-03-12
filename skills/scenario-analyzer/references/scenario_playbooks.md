# Scenario Playbooks — Indian Markets

Templates for building structured scenarios from headlines. Follow the MECE principle: scenarios must be Mutually Exclusive and Collectively Exhaustive (probabilities sum to 100%).

## Scenario Construction Template

### Structure
```
Scenario: [Name]
Probability: [X]%
Timeline: 18 months, divided into 3 phases

Phase 1 (0-6 months): [What happens immediately]
Phase 2 (6-12 months): [How it evolves]
Phase 3 (12-18 months): [End state]

Key Assumptions:
- [What must hold true for this scenario]
- [External conditions required]

Triggers to Watch:
- [What would increase this scenario's probability]
- [What would decrease it]
```

### Probability Distribution Guidelines

| Market Consensus | Base Case | Bull Case | Bear Case |
|-----------------|-----------|-----------|-----------|
| Strong consensus | 50-60% | 20-30% | 15-25% |
| Divided views | 35-45% | 25-35% | 25-35% |
| High uncertainty | 30-40% | 25-35% | 30-40% |

## Playbook 1: RBI Policy Decision

### Base Case (50%): Gradual Easing
- Phase 1: 1-2 rate cuts of 25 bps each
- Phase 2: Transmission to lending rates, credit growth picks up
- Phase 3: GDP acceleration, corporate earnings growth
- Nifty impact: +8-12% over 18 months
- Beneficiaries: Banks, auto, realty, consumer discretionary

### Bull Case (25%): Aggressive Easing
- Phase 1: 50 bps cut + liquidity measures
- Phase 2: Strong credit growth, housing boom
- Phase 3: Capex cycle revival, broad-based rally
- Nifty impact: +15-25% over 18 months
- Beneficiaries: Rate-sensitive sectors, mid/small-caps

### Bear Case (25%): Policy Reversal
- Phase 1: Inflation surprise forces pause or reversal
- Phase 2: Global tightening spills over, INR pressure
- Phase 3: Stagflation risk, earnings downgrades
- Nifty impact: -5-15% over 18 months
- Defensive: Pharma, IT, FMCG

## Playbook 2: Global Risk-Off Event

### Base Case (45%): Contained Impact
- Phase 1: FII outflows ₹20,000-40,000 crore over 2-3 months
- Phase 2: DII absorption, market stabilizes 10% below peak
- Phase 3: FII returns as India growth story intact
- Nifty impact: -10-15% correction, full recovery in 12-15 months

### Bull Case (25%): India Decoupling
- Phase 1: Initial sell-off 5-8%, quick recovery
- Phase 2: India seen as relative safe haven among EMs
- Phase 3: Premium valuation, FII flows accelerate
- Nifty impact: Flat to +5% over 18 months

### Bear Case (30%): Contagion
- Phase 1: FII outflows >₹1 lakh crore, Nifty drops 15-20%
- Phase 2: INR depreciation >5%, imported inflation, RBI forced to tighten
- Phase 3: Earnings downgrades, PE de-rating
- Nifty impact: -20-30% over 18 months

## Playbook 3: Crude Oil Spike

### Base Case (45%): Temporary Spike
- Phase 1: Crude at $90-100, OMC margins compressed
- Phase 2: OPEC+ responds, prices stabilize
- Phase 3: Gradual normalization to $75-85
- Nifty impact: -5-8% correction, recovery in 6 months

### Bull Case (25%): Quick Resolution
- Phase 1: Brief spike above $90, then rapid decline
- Phase 2: Crude settles below $80
- Phase 3: India benefits from lower input costs
- Nifty impact: Brief -3% dip, then +5-10% rally

### Bear Case (30%): Sustained High Prices
- Phase 1: Crude sustained above $100 for 3+ months
- Phase 2: Current account deficit widens, fiscal pressure
- Phase 3: RBI tightens, growth slows
- Nifty impact: -15-20% over 18 months

## Playbook 4: Union Budget

### Base Case (50%): Continuity Budget
- Phase 1: Capex maintained/increased, fiscal discipline continued
- Phase 2: Infrastructure spending flows to order books
- Phase 3: GDP growth sustained at 6.5-7%
- Nifty impact: Neutral to +5% over 6 months

### Bull Case (30%): Reform Budget
- Phase 1: Major tax reforms + capex increase + disinvestment push
- Phase 2: Corporate earnings upgrade cycle
- Phase 3: India valuation re-rating
- Nifty impact: +10-15% over 12 months

### Bear Case (20%): Populist Budget
- Phase 1: Fiscal slippage, populist spending, no reforms
- Phase 2: Bond yields rise, RBI credibility concerns
- Phase 3: Foreign investor confidence hit
- Nifty impact: -5-10% over 6 months

## Impact Cascade Template

```
1° Impact (Immediate, 0-1 month):
  - Sectors: [List with +/- magnitude]
  - Stocks: [3-5 most affected]
  - Mechanism: [Direct causal link]

2° Impact (Short-term, 1-6 months):
  - Sectors: [List with +/- magnitude]
  - Stocks: [3-5 affected through indirect channels]
  - Mechanism: [How 1° effects cascade]

3° Impact (Medium-term, 6-18 months):
  - Sectors: [List with +/- magnitude]
  - Stocks: [3-5 beneficiaries/losers of structural shift]
  - Mechanism: [How 2° effects create new dynamics]
```

## Key Economic Indicators for India

Track these to calibrate scenario probabilities:

| Indicator | Source | Frequency | Impact On |
|-----------|--------|-----------|-----------|
| CPI Inflation | MOSPI | Monthly | RBI policy, rate-sensitive sectors |
| GDP Growth | MOSPI/RBI | Quarterly | Broad market, earnings |
| IIP (Industrial Production) | MOSPI | Monthly | Manufacturing, capital goods |
| Trade Balance | DGFT | Monthly | INR, IT, pharma |
| FII/DII Flows | NSDL/NSE | Daily | Market direction, sector rotation |
| PMI Manufacturing | S&P Global | Monthly | Cyclicals, metals |
| GST Collections | Finance Ministry | Monthly | Consumer, government spending |
| Credit Growth | RBI | Monthly | Banks, economy |
| Auto Sales | SIAM | Monthly | Auto sector, consumer sentiment |
| Cement Production | CMA | Monthly | Infrastructure, realty |
