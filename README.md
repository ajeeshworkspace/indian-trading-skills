# Indian Trading Skills for Claude

> Turn Claude into your Indian market research analyst. 8 specialized skills covering NSE/BSE equities, F&O derivatives, institutional flows, and market breadth — all built for Indian markets.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude Skills](https://img.shields.io/badge/Claude-Skills-blueviolet)](https://claude.ai)

## What This Is

A collection of [Claude Skills](https://docs.anthropic.com/en/docs/claude-code/skills) that give Claude deep knowledge of Indian equity markets. Each skill is a self-contained module with methodology references, scoring frameworks, and Python scripts — purpose-built for NSE/BSE.

**No API keys required** for most skills. Uses free data sources (yfinance, niftystocks) and optionally integrates with [Groww MCP](https://groww.in) for live market data.

Adapted from [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) (US markets) for Indian markets.

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/ajeeshworkspace/indian-trading-skills.git
cd indian-trading-skills
```

### 2. Install dependencies

```bash
pip install -e .

# Or install directly
pip install yfinance pandas scipy pyyaml niftystocks
```

### 3. Add skills to Claude

**Claude Code (CLI):**
Copy the `skills/` directory into your project or point Claude to this repo. Claude automatically discovers `SKILL.md` files.

**Claude Desktop / claude.ai:**
Reference the skill files in your project knowledge or system prompt.

### 4. Start using

Just talk to Claude naturally:

```
"Analyze Reliance Industries stock fundamentals"
"Screen Nifty 500 for VCP breakout setups"
"What's the market impact if RBI cuts rates by 50 bps?"
"Build an iron condor on Bank Nifty for this week's expiry"
"How healthy is the broad market right now?"
"Evaluate my backtest — 150 trades, 58% win rate, 1.8 profit factor"
"What are FII/DII flows telling us this month?"
```

## Skills

### 1. Technical Analyst
Systematic technical analysis of weekly price charts for Indian stocks and indices. Feed it chart images and get structured analysis with probabilistic scenarios.

| | |
|---|---|
| **Trigger** | Provide chart images for analysis |
| **Output** | Trend, S/R levels, MA analysis, volume, 2-4 probability-weighted scenarios |
| **Data** | Chart images (user-provided) |

### 2. NSE VCP Screener
Screens Nifty 50/200/500 for Mark Minervini's Volatility Contraction Pattern — the setup behind many of the biggest stock moves.

| | |
|---|---|
| **Trigger** | "Screen for VCP setups", "Find breakout candidates" |
| **Output** | Ranked candidates with composite scores, pivot levels, risk metrics |
| **Data** | yfinance (free, no API key) |

**Standalone CLI usage:**
```bash
# Screen Nifty 50
python3 skills/nse-vcp-screener/scripts/screen_vcp.py --universe nifty50

# Screen Nifty 500 (broader universe)
python3 skills/nse-vcp-screener/scripts/screen_vcp.py --universe nifty500

# Custom tickers
python3 skills/nse-vcp-screener/scripts/screen_vcp.py --custom-tickers RELIANCE,TCS,INFY,HDFC

# Tune parameters
python3 skills/nse-vcp-screener/scripts/screen_vcp.py --universe nifty200 \
  --min-contractions 2 --t1-depth-min 10 --t1-depth-max 40 \
  --trend-min-score 85 --output-dir reports/
```

**Scoring system:** 5-component composite (Trend Template 25%, Contraction Quality 25%, Volume Dry-Up 20%, Pivot Proximity 15%, Relative Strength 15%).

### 3. India Stock Analysis
Deep fundamental + technical analysis of NSE/BSE stocks. Covers business quality, financials, valuation, shareholding patterns, and peer comparison.

| | |
|---|---|
| **Trigger** | "Analyze TCS", "Compare HDFC Bank vs ICICI Bank" |
| **Output** | Investment report with bull/bear cases, scorecard, risk matrix |
| **Data** | Groww MCP (live) or yfinance (free) |

**India-specific metrics:** Promoter holding/pledge analysis, FII/DII ownership trends, sector-specific ratios (NIM/NPA for banks, ANDA pipeline for pharma, utilization for IT).

### 4. Scenario Analyzer
Builds 18-month probabilistic scenarios from headlines and events. Covers RBI policy, Union Budget, crude oil, elections, monsoons, and global risk events.

| | |
|---|---|
| **Trigger** | Share a news headline or ask about event impact |
| **Output** | 3 scenarios (base/bull/bear) with probabilities, sector impact, portfolio actions |
| **Data** | Built-in reference data (no API needed) |

**Includes:** Historical pattern database (2008-2024), sector sensitivity matrix (10 sectors x 8 event types), and 4 detailed playbooks.

### 5. FII/DII Flow Tracker
Analyzes Foreign and Domestic Institutional Investor flows and their correlation with Nifty direction. Classifies flow regimes and identifies divergences.

| | |
|---|---|
| **Trigger** | "What are FII flows this month?", "Is DII absorbing FII selling?" |
| **Output** | Flow regime assessment, Nifty correlation, sector rotation signals |
| **Data** | Web search (NSDL, NSE data) + Groww MCP |

**Includes:** 4 historical case studies (COVID 2020, Ukraine 2022, Oct 2024, FY2021 rally), flow interpretation decision matrix, FII derivative position analysis.

### 6. Options Strategy Advisor
Recommends and prices options strategies for NSE F&O. Full Black-Scholes engine with Greeks, IV solver, and strategy builders.

| | |
|---|---|
| **Trigger** | "Build a straddle on Nifty", "What's the margin for iron condor?" |
| **Output** | Strategy details, Greeks, margin requirement, ASCII P/L diagram |
| **Data** | Groww MCP (live Greeks, OI, margins) |

**Standalone CLI usage:**
```bash
# Price a call option
python3 skills/options-strategy-advisor/scripts/black_scholes.py price \
  --spot 24000 --strike 24500 --expiry 7 --vol 0.15 --rate 0.065 --type call

# Calculate Greeks
python3 skills/options-strategy-advisor/scripts/black_scholes.py greeks \
  --spot 24000 --strike 24500 --expiry 7 --vol 0.15

# Solve implied volatility
python3 skills/options-strategy-advisor/scripts/black_scholes.py iv \
  --spot 24000 --strike 24500 --expiry 7 --price 120 --type call

# Build iron condor with P/L diagram
python3 skills/options-strategy-advisor/scripts/black_scholes.py strategy \
  --name iron_condor --spot 24000 --expiry 7 --vol 0.15 \
  --strikes 23500 23800 24200 24500
```

**17 strategies supported:** Covered calls, protective puts, bull/bear spreads, straddles, strangles, iron condors, iron butterflies, calendar spreads, diagonal spreads, ratio spreads.

### 7. Backtest Expert
Validates trading strategy backtests with India-specific cost modeling and overfitting detection. Scores across 5 dimensions and delivers a Deploy/Refine/Abandon verdict.

| | |
|---|---|
| **Trigger** | "Evaluate my backtest results", "Is this strategy robust?" |
| **Output** | 0-100 score, red flags, verdict, cost-adjusted metrics |
| **Data** | User-provided backtest results |

**Standalone CLI usage:**
```bash
python3 skills/backtest-expert/scripts/evaluate_backtest.py \
  --trades 150 --win-rate 0.58 --avg-win 2.5 --avg-loss 1.2 \
  --max-drawdown 15 --years 3 --parameters 4 \
  --slippage-modeled --segment delivery --format both
```

**India-specific costs modeled:** STT, stamp duty, exchange transaction charges, SEBI turnover fees, GST — for delivery, intraday, and F&O segments.

### 8. India Market Breadth
Measures internal market health beyond Nifty/Sensex using breadth indicators. Generates a Health Score (0-100) with regime classification.

| | |
|---|---|
| **Trigger** | "How's the broad market?", "Is market breadth healthy?" |
| **Output** | Health score, regime (Risk-On/Cautious/Risk-Off), divergence alerts |
| **Data** | yfinance + Groww MCP |

**5-component scoring:** Advance/Decline (25%), Stocks above 200 DMA (25%), New Highs vs Lows (20%), Sector Participation (15%), Index Divergence (15%).

## Project Structure

```
indian-trading-skills/
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
└── skills/
    ├── technical-analyst/
    │   ├── SKILL.md
    │   ├── references/technical_analysis_framework.md
    │   └── assets/analysis_template.md
    ├── nse-vcp-screener/
    │   ├── SKILL.md
    │   ├── references/{vcp_methodology, scoring_system}.md
    │   └── scripts/{screen_vcp, scorer, report_generator}.py
    │       └── calculators/{trend_template, vcp_pattern, volume_pattern,
    │                        pivot_proximity, relative_strength}_calculator.py
    ├── india-stock-analysis/
    │   ├── SKILL.md
    │   ├── references/{fundamental-analysis, financial-metrics}.md
    │   └── assets/report-template.md
    ├── scenario-analyzer/
    │   ├── SKILL.md
    │   └── references/{headline_event_patterns, sector_sensitivity_matrix,
    │                    scenario_playbooks}.md
    ├── fii-dii-flow-tracker/
    │   ├── SKILL.md
    │   ├── references/{flow_analysis_methodology, flow_interpretation_guide}.md
    │   └── assets/flow_report_template.md
    ├── options-strategy-advisor/
    │   ├── SKILL.md
    │   ├── references/indian_fno_guide.md
    │   └── scripts/black_scholes.py
    ├── backtest-expert/
    │   ├── SKILL.md
    │   ├── references/{methodology, failed_tests}.md
    │   └── scripts/evaluate_backtest.py
    └── india-market-breadth/
        ├── SKILL.md
        ├── references/breadth_methodology.md
        └── assets/breadth_report_template.md
```

## Data Sources

| Source | Skills | API Key | Cost |
|--------|--------|---------|------|
| [yfinance](https://github.com/ranaroussi/yfinance) | VCP Screener, Market Breadth | None | Free |
| [niftystocks](https://github.com/swapniljariwala/niftystocks) | VCP Screener | None | Free |
| [Groww MCP](https://groww.in) | Stock Analysis, Options, Flows | Via Claude | Free |
| Web Search | Flow Tracker, Scenario Analyzer | Via Claude | Free |

## Indian Market Context

| Detail | Value |
|--------|-------|
| Exchanges | NSE (primary), BSE |
| Currency | INR (all prices in rupees) |
| Trading Hours | 9:15 AM – 3:30 PM IST |
| Settlement | T+1 for equities |
| F&O Expiry | Weekly (Thu) for index options, monthly for stock options |
| Circuit Limits | 2%, 5%, 10%, 20% daily limits |
| Regulator | SEBI |
| Key Indices | Nifty 50, Sensex, Bank Nifty, Nifty IT, Nifty Pharma |

## Contributing

Contributions welcome! Some ideas:

- **New skills**: CANSLIM screener, earnings calendar, promoter pledge monitor, IPO analyzer
- **Enhancements**: Tests for existing calculators, more sector-specific analysis frameworks
- **Data sources**: Additional free data integrations (NSE API, BSE API)
- **Documentation**: Usage examples, video walkthroughs

Please open an issue first to discuss significant changes.

## Disclaimer

This project is for **educational and research purposes only**. It does not constitute financial advice. Always do your own research before making investment decisions. The authors are not SEBI-registered investment advisors.

Past performance of any strategy, indicator, or methodology does not guarantee future results. Trading in equities and derivatives involves substantial risk of loss.

## License

[MIT](LICENSE) — use it, fork it, build on it.

## Credits

- Upstream: [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) (US markets)
- Methodology: Mark Minervini (VCP/Trend Template), William O'Neil (CANSLIM concepts)
- Data: [Yahoo Finance](https://finance.yahoo.com), [Groww](https://groww.in), [NSE India](https://www.nseindia.com)
