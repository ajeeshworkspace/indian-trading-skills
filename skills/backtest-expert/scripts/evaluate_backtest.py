#!/usr/bin/env python3
"""
Backtest Evaluation Scoring Tool for Indian Markets (NSE/BSE)

Evaluates a completed backtest across 5 dimensions (20 points each = 100 total):
  1. Sample Size        — Statistical significance of trade count
  2. Expectancy         — Edge per trade after Indian market costs
  3. Risk Management    — Drawdown control and profit factor
  4. Robustness         — Years tested and parameter parsimony
  5. Execution Realism  — Whether slippage/friction was modeled

Outputs JSON and/or Markdown report with verdict: Deploy / Refine / Abandon.

Usage:
  python3 evaluate_backtest.py \
    --total-trades 150 \
    --win-rate 62 \
    --avg-win-pct 1.8 \
    --avg-loss-pct 1.2 \
    --max-drawdown-pct 15 \
    --years-tested 8 \
    --num-parameters 3 \
    --slippage-tested

  python3 evaluate_backtest.py \
    --total-trades 150 \
    --win-rate 62 \
    --avg-win-pct 1.8 \
    --avg-loss-pct 1.2 \
    --max-drawdown-pct 15 \
    --years-tested 8 \
    --num-parameters 3 \
    --slippage-tested \
    --output json \
    --include-india-costs \
    --brokerage-per-trade 20 \
    --avg-trade-value 50000
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DimensionScore:
    """Score for a single evaluation dimension."""
    name: str
    score: float
    max_score: float
    details: str
    sub_scores: dict = field(default_factory=dict)


@dataclass
class RedFlag:
    """A detected red flag in the backtest."""
    severity: str  # "critical", "warning", "info"
    message: str
    recommendation: str


@dataclass
class EvaluationResult:
    """Complete evaluation output."""
    total_score: float
    max_possible: float
    percentage: float
    verdict: str
    verdict_detail: str
    dimensions: List[DimensionScore] = field(default_factory=list)
    red_flags: List[RedFlag] = field(default_factory=list)
    raw_expectancy: float = 0.0
    adjusted_expectancy: float = 0.0
    india_cost_impact: Optional[dict] = None
    input_parameters: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# India-specific cost calculations
# ---------------------------------------------------------------------------

def calculate_india_costs(
    avg_trade_value: float,
    brokerage_per_trade: float = 20.0,
    trade_type: str = "delivery",
) -> dict:
    """
    Calculate round-trip transaction costs for Indian markets.

    Args:
        avg_trade_value: Average trade value in INR.
        brokerage_per_trade: Flat brokerage per order (default Rs 20 for discount broker).
        trade_type: One of 'delivery', 'intraday', 'fno_options', 'fno_futures'.

    Returns:
        Dictionary with cost breakdown and total round-trip cost as percentage.
    """
    costs = {}

    # Brokerage (buy + sell)
    brokerage_total = brokerage_per_trade * 2
    costs["brokerage"] = brokerage_total
    costs["brokerage_pct"] = (brokerage_total / avg_trade_value) * 100

    # STT (Securities Transaction Tax)
    if trade_type == "delivery":
        stt = avg_trade_value * 0.001 * 2  # 0.1% on buy + sell
    elif trade_type == "intraday":
        stt = avg_trade_value * 0.00025  # 0.025% on sell only
    elif trade_type == "fno_options":
        stt = avg_trade_value * 0.000125  # 0.0125% on sell (options, on premium)
    elif trade_type == "fno_futures":
        stt = avg_trade_value * 0.000125  # 0.0125% on sell
    else:
        stt = avg_trade_value * 0.001 * 2  # Default to delivery

    costs["stt"] = stt
    costs["stt_pct"] = (stt / avg_trade_value) * 100

    # Exchange transaction charges (NSE)
    if trade_type in ("fno_options",):
        exchange_rate = 0.0005  # 0.05% for options
    else:
        exchange_rate = 0.0000345  # 0.00345% for equity

    exchange_charges = avg_trade_value * exchange_rate * 2  # Buy + sell
    costs["exchange_charges"] = exchange_charges
    costs["exchange_charges_pct"] = (exchange_charges / avg_trade_value) * 100

    # GST (18% on brokerage + exchange charges)
    gst_base = brokerage_total + exchange_charges
    gst = gst_base * 0.18
    costs["gst"] = gst
    costs["gst_pct"] = (gst / avg_trade_value) * 100

    # Stamp duty (on buy side)
    if trade_type == "delivery":
        stamp_duty = avg_trade_value * 0.00015  # 0.015%
    else:
        stamp_duty = avg_trade_value * 0.00003  # 0.003%

    costs["stamp_duty"] = stamp_duty
    costs["stamp_duty_pct"] = (stamp_duty / avg_trade_value) * 100

    # SEBI charges
    sebi_charges = avg_trade_value * 0.000001 * 2  # 0.0001% buy + sell
    costs["sebi_charges"] = sebi_charges
    costs["sebi_charges_pct"] = (sebi_charges / avg_trade_value) * 100

    # Total
    total_cost = sum([
        brokerage_total, stt, exchange_charges, gst, stamp_duty, sebi_charges
    ])
    costs["total_round_trip"] = total_cost
    costs["total_round_trip_pct"] = (total_cost / avg_trade_value) * 100
    costs["trade_type"] = trade_type

    return costs


# ---------------------------------------------------------------------------
# Dimension scoring functions
# ---------------------------------------------------------------------------

def score_sample_size(total_trades: int) -> DimensionScore:
    """
    Dimension 1: Sample Size (0-20 points).

    Scoring:
      < 30 trades:    0-5 pts  (statistically meaningless)
      30-49 trades:   5-8 pts  (bare minimum)
      50-99 trades:   8-12 pts (weak but usable)
      100-149 trades: 12-15 pts (moderate confidence)
      150-199 trades: 15-18 pts (good confidence)
      200+ trades:    18-20 pts (strong confidence)
    """
    if total_trades < 30:
        score = max(0, total_trades / 6)  # 0-5
        quality = "Statistically meaningless"
    elif total_trades < 50:
        score = 5 + (total_trades - 30) * (3 / 20)  # 5-8
        quality = "Bare minimum"
    elif total_trades < 100:
        score = 8 + (total_trades - 50) * (4 / 50)  # 8-12
        quality = "Weak but usable"
    elif total_trades < 150:
        score = 12 + (total_trades - 100) * (3 / 50)  # 12-15
        quality = "Moderate confidence"
    elif total_trades < 200:
        score = 15 + (total_trades - 150) * (3 / 50)  # 15-18
        quality = "Good confidence"
    else:
        score = 18 + min(2, (total_trades - 200) / 100)  # 18-20
        quality = "Strong confidence"

    score = round(min(20, score), 1)

    return DimensionScore(
        name="Sample Size",
        score=score,
        max_score=20.0,
        details=f"{total_trades} trades — {quality}",
        sub_scores={
            "total_trades": total_trades,
            "quality_label": quality,
        },
    )


def score_expectancy(
    win_rate: float,
    avg_win_pct: float,
    avg_loss_pct: float,
    cost_pct: float = 0.0,
) -> DimensionScore:
    """
    Dimension 2: Expectancy (0-20 points).

    Expectancy = (win_rate * avg_win) - (loss_rate * avg_loss) - costs_per_trade

    Scoring:
      E <= 0:        0 pts   (no edge)
      E 0-0.1%:      0-5 pts (marginal edge, may vanish with costs)
      E 0.1-0.3%:    5-10 pts (small but real edge)
      E 0.3-0.6%:    10-15 pts (solid edge)
      E 0.6-1.0%:    15-18 pts (strong edge)
      E > 1.0%:      18-20 pts (exceptional — verify it is real)
    """
    win_rate_decimal = win_rate / 100.0
    loss_rate_decimal = 1.0 - win_rate_decimal

    raw_expectancy = (win_rate_decimal * avg_win_pct) - (loss_rate_decimal * avg_loss_pct)
    adjusted_expectancy = raw_expectancy - cost_pct

    e = adjusted_expectancy

    if e <= 0:
        score = 0
        quality = "No edge (negative or zero expectancy)"
    elif e <= 0.1:
        score = e / 0.1 * 5  # 0-5
        quality = "Marginal edge — may vanish with real costs"
    elif e <= 0.3:
        score = 5 + (e - 0.1) / 0.2 * 5  # 5-10
        quality = "Small but real edge"
    elif e <= 0.6:
        score = 10 + (e - 0.3) / 0.3 * 5  # 10-15
        quality = "Solid edge"
    elif e <= 1.0:
        score = 15 + (e - 0.6) / 0.4 * 3  # 15-18
        quality = "Strong edge"
    else:
        score = 18 + min(2, (e - 1.0) / 0.5)  # 18-20
        quality = "Exceptional edge — verify it is real"

    score = round(min(20, score), 1)

    # Profit factor
    gross_profit = win_rate_decimal * avg_win_pct
    gross_loss = loss_rate_decimal * avg_loss_pct
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    return DimensionScore(
        name="Expectancy",
        score=score,
        max_score=20.0,
        details=(
            f"Raw E = {raw_expectancy:.4f}%, "
            f"Adjusted E = {adjusted_expectancy:.4f}% (after {cost_pct:.4f}% costs), "
            f"Profit Factor = {profit_factor:.2f} — {quality}"
        ),
        sub_scores={
            "raw_expectancy_pct": round(raw_expectancy, 4),
            "adjusted_expectancy_pct": round(adjusted_expectancy, 4),
            "cost_pct_per_trade": round(cost_pct, 4),
            "profit_factor": round(profit_factor, 2),
            "quality_label": quality,
        },
    )


def score_risk_management(
    max_drawdown_pct: float,
    win_rate: float,
    avg_win_pct: float,
    avg_loss_pct: float,
) -> DimensionScore:
    """
    Dimension 3: Risk Management (0-20 points).

    Two sub-components:
      A. Max Drawdown Score (0-12 points):
         < 10%:  10-12 pts
         10-15%: 8-10 pts
         15-25%: 5-8 pts
         25-35%: 2-5 pts
         > 35%:  0-2 pts

      B. Profit Factor Score (0-8 points):
         PF > 2.0:   7-8 pts
         PF 1.5-2.0: 5-7 pts
         PF 1.2-1.5: 3-5 pts
         PF 1.0-1.2: 1-3 pts
         PF < 1.0:   0 pts
    """
    # Sub-score A: Max Drawdown
    if max_drawdown_pct < 10:
        dd_score = 10 + (10 - max_drawdown_pct) / 10 * 2  # 10-12
    elif max_drawdown_pct < 15:
        dd_score = 8 + (15 - max_drawdown_pct) / 5 * 2  # 8-10
    elif max_drawdown_pct < 25:
        dd_score = 5 + (25 - max_drawdown_pct) / 10 * 3  # 5-8
    elif max_drawdown_pct < 35:
        dd_score = 2 + (35 - max_drawdown_pct) / 10 * 3  # 2-5
    else:
        dd_score = max(0, 2 - (max_drawdown_pct - 35) / 15 * 2)  # 0-2

    dd_score = round(min(12, max(0, dd_score)), 1)

    # Sub-score B: Profit Factor
    win_rate_decimal = win_rate / 100.0
    loss_rate_decimal = 1.0 - win_rate_decimal
    gross_profit = win_rate_decimal * avg_win_pct
    gross_loss = loss_rate_decimal * avg_loss_pct
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    if profit_factor >= 2.0:
        pf_score = 7 + min(1, (profit_factor - 2.0) / 1.0)  # 7-8
    elif profit_factor >= 1.5:
        pf_score = 5 + (profit_factor - 1.5) / 0.5 * 2  # 5-7
    elif profit_factor >= 1.2:
        pf_score = 3 + (profit_factor - 1.2) / 0.3 * 2  # 3-5
    elif profit_factor >= 1.0:
        pf_score = 1 + (profit_factor - 1.0) / 0.2 * 2  # 1-3
    else:
        pf_score = 0

    pf_score = round(min(8, max(0, pf_score)), 1)

    total_score = round(dd_score + pf_score, 1)

    return DimensionScore(
        name="Risk Management",
        score=total_score,
        max_score=20.0,
        details=(
            f"Max Drawdown: {max_drawdown_pct}% (score {dd_score}/12), "
            f"Profit Factor: {profit_factor:.2f} (score {pf_score}/8)"
        ),
        sub_scores={
            "max_drawdown_pct": max_drawdown_pct,
            "drawdown_score": dd_score,
            "profit_factor": round(profit_factor, 2),
            "profit_factor_score": pf_score,
        },
    )


def score_robustness(years_tested: float, num_parameters: int) -> DimensionScore:
    """
    Dimension 4: Robustness (0-20 points).

    Two sub-components:
      A. Years Tested (0-12 points):
         < 3 years:    0-4 pts
         3-5 years:    4-7 pts
         5-8 years:    7-10 pts
         8-10 years:   10-11 pts
         10+ years:    11-12 pts

      B. Parameter Parsimony (0-8 points):
         1-2 params:   7-8 pts (simple, robust)
         3-4 params:   5-7 pts (acceptable)
         5-6 params:   2-5 pts (getting complex)
         7+ params:    0-2 pts (likely overfit)
    """
    # Sub-score A: Years tested
    if years_tested < 3:
        years_score = years_tested / 3 * 4  # 0-4
    elif years_tested < 5:
        years_score = 4 + (years_tested - 3) / 2 * 3  # 4-7
    elif years_tested < 8:
        years_score = 7 + (years_tested - 5) / 3 * 3  # 7-10
    elif years_tested < 10:
        years_score = 10 + (years_tested - 8) / 2 * 1  # 10-11
    else:
        years_score = 11 + min(1, (years_tested - 10) / 5)  # 11-12

    years_score = round(min(12, max(0, years_score)), 1)

    # Sub-score B: Parameter count
    if num_parameters <= 2:
        param_score = 7 + (2 - num_parameters) * 0.5  # 7-8
    elif num_parameters <= 4:
        param_score = 5 + (4 - num_parameters) / 2 * 2  # 5-7
    elif num_parameters <= 6:
        param_score = 2 + (6 - num_parameters) / 2 * 3  # 2-5
    else:
        param_score = max(0, 2 - (num_parameters - 6) * 0.5)  # 0-2

    param_score = round(min(8, max(0, param_score)), 1)

    total_score = round(years_score + param_score, 1)

    return DimensionScore(
        name="Robustness",
        score=total_score,
        max_score=20.0,
        details=(
            f"{years_tested} years tested (score {years_score}/12), "
            f"{num_parameters} parameters (score {param_score}/8)"
        ),
        sub_scores={
            "years_tested": years_tested,
            "years_score": years_score,
            "num_parameters": num_parameters,
            "parameter_score": param_score,
        },
    )


def score_execution_realism(slippage_tested: bool) -> DimensionScore:
    """
    Dimension 5: Execution Realism (0-20 points).

    Binary for now — did the backtest model slippage and transaction costs?
      Yes: 20 pts
      No:  5 pts (some credit for doing a backtest at all, but major penalty)
    """
    if slippage_tested:
        score = 20.0
        details = "Slippage and execution friction were modeled — full marks"
    else:
        score = 5.0
        details = (
            "Slippage/friction NOT modeled — results are likely optimistic. "
            "For Indian markets, expect 0.1-0.5% round-trip cost reduction."
        )

    return DimensionScore(
        name="Execution Realism",
        score=score,
        max_score=20.0,
        details=details,
        sub_scores={"slippage_tested": slippage_tested},
    )


# ---------------------------------------------------------------------------
# Red flag detection
# ---------------------------------------------------------------------------

def detect_red_flags(
    total_trades: int,
    win_rate: float,
    avg_win_pct: float,
    avg_loss_pct: float,
    max_drawdown_pct: float,
    years_tested: float,
    num_parameters: int,
    slippage_tested: bool,
    adjusted_expectancy: float,
) -> List[RedFlag]:
    """Detect red flags and warnings in the backtest results."""
    flags = []

    # Critical: Negative expectancy
    if adjusted_expectancy <= 0:
        flags.append(RedFlag(
            severity="critical",
            message="Negative or zero expectancy after costs — no trading edge exists.",
            recommendation=(
                "Re-examine the hypothesis. Either the edge does not exist, "
                "or transaction costs destroy it. Consider wider targets or "
                "lower-frequency trading to reduce cost impact."
            ),
        ))

    # Critical: Tiny sample
    if total_trades < 30:
        flags.append(RedFlag(
            severity="critical",
            message=f"Only {total_trades} trades — statistically meaningless.",
            recommendation=(
                "Expand the universe, extend the time period, or lower entry "
                "thresholds to generate more trades. Minimum 100 trades for "
                "any confidence."
            ),
        ))

    # Critical: Too many parameters
    if num_parameters > 5:
        flags.append(RedFlag(
            severity="critical",
            message=f"{num_parameters} parameters — high risk of overfitting.",
            recommendation=(
                "Reduce free parameters to 3-4. Each additional parameter "
                "increases the risk of curve-fitting. Ask: does removing this "
                "parameter destroy the strategy, or just reduce backtest returns?"
            ),
        ))

    # Critical: Slippage not tested
    if not slippage_tested:
        flags.append(RedFlag(
            severity="critical",
            message="Slippage and execution friction not modeled.",
            recommendation=(
                "Re-run with realistic costs. For NSE: add 0.05-0.1% slippage "
                "for large-caps, 0.1-0.3% for mid/small-caps, plus brokerage "
                "(Rs 20/order), STT (0.1% delivery), and other charges."
            ),
        ))

    # Warning: Suspiciously high win rate
    if win_rate > 80:
        flags.append(RedFlag(
            severity="warning",
            message=f"Win rate of {win_rate}% is suspiciously high.",
            recommendation=(
                "Verify that fills are realistic. Check for look-ahead bias "
                "(using future data for entry/exit decisions). High win rates "
                "often come with large average losses — check risk/reward ratio."
            ),
        ))

    # Warning: Short test period
    if years_tested < 5:
        flags.append(RedFlag(
            severity="warning",
            message=f"Only {years_tested} years tested — may miss market regime changes.",
            recommendation=(
                "Extend to at least 5 years, ideally 8-10. Indian markets "
                "had distinct regimes: 2008 crash, 2014-17 bull, 2018-19 "
                "sideways, 2020 COVID crash/recovery, 2021 broad bull, "
                "2022 selective, 2023-24 mixed."
            ),
        ))

    # Warning: Large drawdown
    if max_drawdown_pct > 30:
        flags.append(RedFlag(
            severity="warning",
            message=f"Max drawdown of {max_drawdown_pct}% is psychologically challenging.",
            recommendation=(
                "Most traders abandon strategies during 25%+ drawdowns. "
                "Consider reducing position size, adding a drawdown circuit "
                "breaker (e.g., pause after 15% drawdown), or tightening stops."
            ),
        ))

    # Warning: Marginal expectancy
    if 0 < adjusted_expectancy < 0.1:
        flags.append(RedFlag(
            severity="warning",
            message=f"Expectancy of {adjusted_expectancy:.4f}% is marginal.",
            recommendation=(
                "This edge is close to zero and may disappear with slight "
                "changes in market conditions, slippage, or costs. Consider "
                "whether the edge is large enough to be worth the effort."
            ),
        ))

    # Info: Moderate sample
    if 30 <= total_trades < 100:
        flags.append(RedFlag(
            severity="info",
            message=f"{total_trades} trades is below the recommended 100+ threshold.",
            recommendation=(
                "Results are directionally useful but confidence intervals "
                "are wide. Try to increase sample size before deploying capital."
            ),
        ))

    # Info: Win/loss asymmetry check
    if avg_loss_pct > avg_win_pct * 2:
        flags.append(RedFlag(
            severity="warning",
            message=(
                f"Average loss ({avg_loss_pct}%) is more than 2x average win "
                f"({avg_win_pct}%). Risk/reward is inverted."
            ),
            recommendation=(
                "This pattern (high win rate, large losses) is fragile. "
                "A few bad trades can wipe out many winners. Consider "
                "tightening stops or widening targets."
            ),
        ))

    return flags


# ---------------------------------------------------------------------------
# Verdict logic
# ---------------------------------------------------------------------------

def determine_verdict(total_score: float) -> tuple:
    """Return (verdict, detail) based on total score."""
    if total_score >= 80:
        return (
            "DEPLOY",
            (
                "Strategy shows strong evidence of a real edge. Start with 25% "
                "of intended size and scale up after 50+ live trades confirm "
                "out-of-sample performance."
            ),
        )
    elif total_score >= 60:
        return (
            "REFINE",
            (
                "Strategy has potential but needs improvement. Identify the "
                "weakest scoring dimension and address it. Re-run evaluation "
                "after changes."
            ),
        )
    elif total_score >= 40:
        return (
            "REFINE WITH CAUTION",
            (
                "Multiple dimensions are weak. The strategy may be salvageable "
                "but requires significant rework. Consider whether the "
                "hypothesis itself is valid before investing more time."
            ),
        )
    else:
        return (
            "ABANDON",
            (
                "The backtest does not provide evidence of a tradeable edge. "
                "Document what you learned and move on to a different hypothesis. "
                "Failed backtests are valuable — they narrow the search space."
            ),
        )


# ---------------------------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------------------------

def evaluate_backtest(
    total_trades: int,
    win_rate: float,
    avg_win_pct: float,
    avg_loss_pct: float,
    max_drawdown_pct: float,
    years_tested: float,
    num_parameters: int,
    slippage_tested: bool = False,
    include_india_costs: bool = False,
    brokerage_per_trade: float = 20.0,
    avg_trade_value: float = 50000.0,
    trade_type: str = "delivery",
) -> EvaluationResult:
    """Run full 5-dimension evaluation and return result."""

    # Calculate India-specific costs if requested
    india_costs = None
    cost_pct_per_trade = 0.0

    if include_india_costs:
        india_costs = calculate_india_costs(
            avg_trade_value=avg_trade_value,
            brokerage_per_trade=brokerage_per_trade,
            trade_type=trade_type,
        )
        cost_pct_per_trade = india_costs["total_round_trip_pct"]

    # Score each dimension
    d1 = score_sample_size(total_trades)
    d2 = score_expectancy(win_rate, avg_win_pct, avg_loss_pct, cost_pct_per_trade)
    d3 = score_risk_management(max_drawdown_pct, win_rate, avg_win_pct, avg_loss_pct)
    d4 = score_robustness(years_tested, num_parameters)
    d5 = score_execution_realism(slippage_tested)

    dimensions = [d1, d2, d3, d4, d5]
    total_score = round(sum(d.score for d in dimensions), 1)
    max_possible = sum(d.max_score for d in dimensions)
    percentage = round(total_score / max_possible * 100, 1)

    # Raw and adjusted expectancy for the result
    win_rate_decimal = win_rate / 100.0
    loss_rate_decimal = 1.0 - win_rate_decimal
    raw_expectancy = (win_rate_decimal * avg_win_pct) - (loss_rate_decimal * avg_loss_pct)
    adjusted_expectancy = raw_expectancy - cost_pct_per_trade

    # Detect red flags
    red_flags = detect_red_flags(
        total_trades=total_trades,
        win_rate=win_rate,
        avg_win_pct=avg_win_pct,
        avg_loss_pct=avg_loss_pct,
        max_drawdown_pct=max_drawdown_pct,
        years_tested=years_tested,
        num_parameters=num_parameters,
        slippage_tested=slippage_tested,
        adjusted_expectancy=adjusted_expectancy,
    )

    # Determine verdict
    verdict, verdict_detail = determine_verdict(total_score)

    # Override verdict if critical red flags exist
    critical_flags = [f for f in red_flags if f.severity == "critical"]
    if critical_flags and verdict == "DEPLOY":
        verdict = "REFINE"
        verdict_detail = (
            f"Score qualifies for deployment, but {len(critical_flags)} critical "
            f"red flag(s) detected. Address these before deploying: "
            + "; ".join(f.message for f in critical_flags)
        )

    return EvaluationResult(
        total_score=total_score,
        max_possible=max_possible,
        percentage=percentage,
        verdict=verdict,
        verdict_detail=verdict_detail,
        dimensions=dimensions,
        red_flags=red_flags,
        raw_expectancy=round(raw_expectancy, 4),
        adjusted_expectancy=round(adjusted_expectancy, 4),
        india_cost_impact=india_costs,
        input_parameters={
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_win_pct": avg_win_pct,
            "avg_loss_pct": avg_loss_pct,
            "max_drawdown_pct": max_drawdown_pct,
            "years_tested": years_tested,
            "num_parameters": num_parameters,
            "slippage_tested": slippage_tested,
            "include_india_costs": include_india_costs,
            "brokerage_per_trade": brokerage_per_trade,
            "avg_trade_value": avg_trade_value,
            "trade_type": trade_type,
        },
    )


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def result_to_dict(result: EvaluationResult) -> dict:
    """Convert result to a JSON-serializable dictionary."""
    return {
        "total_score": result.total_score,
        "max_possible": result.max_possible,
        "percentage": result.percentage,
        "verdict": result.verdict,
        "verdict_detail": result.verdict_detail,
        "raw_expectancy_pct": result.raw_expectancy,
        "adjusted_expectancy_pct": result.adjusted_expectancy,
        "dimensions": [
            {
                "name": d.name,
                "score": d.score,
                "max_score": d.max_score,
                "details": d.details,
                "sub_scores": d.sub_scores,
            }
            for d in result.dimensions
        ],
        "red_flags": [
            {
                "severity": f.severity,
                "message": f.message,
                "recommendation": f.recommendation,
            }
            for f in result.red_flags
        ],
        "india_cost_impact": result.india_cost_impact,
        "input_parameters": result.input_parameters,
    }


def result_to_markdown(result: EvaluationResult) -> str:
    """Format result as a readable Markdown report."""
    lines = []

    # Header
    lines.append("# Backtest Evaluation Report")
    lines.append("")

    # Score summary
    bar_filled = int(result.percentage / 5)
    bar_empty = 20 - bar_filled
    bar = "[" + "#" * bar_filled + "-" * bar_empty + "]"
    lines.append(f"## Overall Score: {result.total_score} / {result.max_possible} ({result.percentage}%)")
    lines.append(f"```")
    lines.append(f"  {bar} {result.percentage}%")
    lines.append(f"```")
    lines.append("")

    # Verdict
    lines.append(f"## Verdict: {result.verdict}")
    lines.append(f"> {result.verdict_detail}")
    lines.append("")

    # Expectancy
    lines.append(f"## Expectancy")
    lines.append(f"- Raw Expectancy: **{result.raw_expectancy}%** per trade")
    lines.append(f"- Adjusted Expectancy: **{result.adjusted_expectancy}%** per trade (after costs)")
    lines.append("")

    # Dimension breakdown
    lines.append("## Dimension Scores")
    lines.append("")
    lines.append("| # | Dimension | Score | Max | Details |")
    lines.append("|---|-----------|-------|-----|---------|")
    for i, d in enumerate(result.dimensions, 1):
        lines.append(f"| {i} | {d.name} | {d.score} | {d.max_score} | {d.details} |")
    lines.append("")

    # India cost impact
    if result.india_cost_impact:
        costs = result.india_cost_impact
        lines.append("## India Transaction Cost Breakdown")
        lines.append(f"- Trade Type: **{costs['trade_type']}**")
        lines.append(f"- Brokerage: Rs {costs['brokerage']:.2f} ({costs['brokerage_pct']:.4f}%)")
        lines.append(f"- STT: Rs {costs['stt']:.2f} ({costs['stt_pct']:.4f}%)")
        lines.append(f"- Exchange Charges: Rs {costs['exchange_charges']:.2f} ({costs['exchange_charges_pct']:.4f}%)")
        lines.append(f"- GST: Rs {costs['gst']:.2f} ({costs['gst_pct']:.4f}%)")
        lines.append(f"- Stamp Duty: Rs {costs['stamp_duty']:.2f} ({costs['stamp_duty_pct']:.4f}%)")
        lines.append(f"- SEBI Charges: Rs {costs['sebi_charges']:.2f} ({costs['sebi_charges_pct']:.4f}%)")
        lines.append(f"- **Total Round-trip: Rs {costs['total_round_trip']:.2f} ({costs['total_round_trip_pct']:.4f}%)**")
        lines.append("")

    # Red flags
    if result.red_flags:
        lines.append("## Red Flags & Warnings")
        lines.append("")
        for flag in result.red_flags:
            icon = {"critical": "[CRITICAL]", "warning": "[WARNING]", "info": "[INFO]"}
            lines.append(f"### {icon.get(flag.severity, '[FLAG]')} {flag.message}")
            lines.append(f"> {flag.recommendation}")
            lines.append("")
    else:
        lines.append("## Red Flags & Warnings")
        lines.append("No red flags detected.")
        lines.append("")

    # Input parameters
    lines.append("## Input Parameters")
    params = result.input_parameters
    lines.append(f"- Total Trades: {params['total_trades']}")
    lines.append(f"- Win Rate: {params['win_rate']}%")
    lines.append(f"- Average Win: {params['avg_win_pct']}%")
    lines.append(f"- Average Loss: {params['avg_loss_pct']}%")
    lines.append(f"- Max Drawdown: {params['max_drawdown_pct']}%")
    lines.append(f"- Years Tested: {params['years_tested']}")
    lines.append(f"- Number of Parameters: {params['num_parameters']}")
    lines.append(f"- Slippage Tested: {'Yes' if params['slippage_tested'] else 'No'}")
    if params.get("include_india_costs"):
        lines.append(f"- India Costs Included: Yes")
        lines.append(f"- Brokerage per Trade: Rs {params['brokerage_per_trade']}")
        lines.append(f"- Average Trade Value: Rs {params['avg_trade_value']}")
        lines.append(f"- Trade Type: {params['trade_type']}")
    lines.append("")

    # CLI command to reproduce
    lines.append("## Reproduce This Evaluation")
    lines.append("```bash")
    cmd_parts = [
        "python3 evaluate_backtest.py",
        f"  --total-trades {params['total_trades']}",
        f"  --win-rate {params['win_rate']}",
        f"  --avg-win-pct {params['avg_win_pct']}",
        f"  --avg-loss-pct {params['avg_loss_pct']}",
        f"  --max-drawdown-pct {params['max_drawdown_pct']}",
        f"  --years-tested {params['years_tested']}",
        f"  --num-parameters {params['num_parameters']}",
    ]
    if params["slippage_tested"]:
        cmd_parts.append("  --slippage-tested")
    if params.get("include_india_costs"):
        cmd_parts.append("  --include-india-costs")
        cmd_parts.append(f"  --brokerage-per-trade {params['brokerage_per_trade']}")
        cmd_parts.append(f"  --avg-trade-value {params['avg_trade_value']}")
        cmd_parts.append(f"  --trade-type {params['trade_type']}")
    lines.append(" \\\n".join(cmd_parts))
    lines.append("```")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate a completed backtest across 5 dimensions (100-point scale). "
            "Designed for Indian market strategies (NSE/BSE)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic evaluation
  python3 evaluate_backtest.py --total-trades 150 --win-rate 62 \\
    --avg-win-pct 1.8 --avg-loss-pct 1.2 --max-drawdown-pct 15 \\
    --years-tested 8 --num-parameters 3 --slippage-tested

  # With India-specific cost analysis
  python3 evaluate_backtest.py --total-trades 200 --win-rate 55 \\
    --avg-win-pct 2.5 --avg-loss-pct 1.5 --max-drawdown-pct 20 \\
    --years-tested 10 --num-parameters 4 --slippage-tested \\
    --include-india-costs --avg-trade-value 100000 --trade-type delivery

  # JSON output for programmatic use
  python3 evaluate_backtest.py --total-trades 150 --win-rate 62 \\
    --avg-win-pct 1.8 --avg-loss-pct 1.2 --max-drawdown-pct 15 \\
    --years-tested 8 --num-parameters 3 --output json

Scoring:
  80-100 = DEPLOY    | 60-79 = REFINE
  40-59  = REFINE WITH CAUTION | 0-39  = ABANDON
        """,
    )

    # Required parameters
    parser.add_argument(
        "--total-trades", type=int, required=True,
        help="Total number of trades in the backtest",
    )
    parser.add_argument(
        "--win-rate", type=float, required=True,
        help="Win rate as percentage (e.g., 62 for 62%%)",
    )
    parser.add_argument(
        "--avg-win-pct", type=float, required=True,
        help="Average winning trade return in %% (e.g., 1.8 for 1.8%%)",
    )
    parser.add_argument(
        "--avg-loss-pct", type=float, required=True,
        help="Average losing trade return in %% as a positive number (e.g., 1.2 for -1.2%%)",
    )
    parser.add_argument(
        "--max-drawdown-pct", type=float, required=True,
        help="Maximum drawdown in %% (e.g., 15 for 15%%)",
    )
    parser.add_argument(
        "--years-tested", type=float, required=True,
        help="Number of years of historical data tested",
    )
    parser.add_argument(
        "--num-parameters", type=int, required=True,
        help="Number of free/optimizable parameters in the strategy",
    )

    # Optional flags
    parser.add_argument(
        "--slippage-tested", action="store_true", default=False,
        help="Flag indicating slippage and execution friction were modeled",
    )

    # India cost modeling
    parser.add_argument(
        "--include-india-costs", action="store_true", default=False,
        help="Calculate and include India-specific transaction costs in expectancy",
    )
    parser.add_argument(
        "--brokerage-per-trade", type=float, default=20.0,
        help="Brokerage per order in INR (default: 20 for discount brokers)",
    )
    parser.add_argument(
        "--avg-trade-value", type=float, default=50000.0,
        help="Average trade value in INR (default: 50000)",
    )
    parser.add_argument(
        "--trade-type", type=str, default="delivery",
        choices=["delivery", "intraday", "fno_options", "fno_futures"],
        help="Type of trade for cost calculation (default: delivery)",
    )

    # Output format
    parser.add_argument(
        "--output", type=str, default="markdown",
        choices=["markdown", "json", "both"],
        help="Output format (default: markdown)",
    )

    return parser


def main():
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # Validate inputs
    if args.win_rate < 0 or args.win_rate > 100:
        parser.error("--win-rate must be between 0 and 100")
    if args.avg_win_pct < 0:
        parser.error("--avg-win-pct must be non-negative")
    if args.avg_loss_pct < 0:
        parser.error("--avg-loss-pct must be non-negative (enter as positive number)")
    if args.max_drawdown_pct < 0:
        parser.error("--max-drawdown-pct must be non-negative")
    if args.total_trades < 1:
        parser.error("--total-trades must be at least 1")
    if args.years_tested <= 0:
        parser.error("--years-tested must be positive")
    if args.num_parameters < 0:
        parser.error("--num-parameters must be non-negative")

    # Run evaluation
    result = evaluate_backtest(
        total_trades=args.total_trades,
        win_rate=args.win_rate,
        avg_win_pct=args.avg_win_pct,
        avg_loss_pct=args.avg_loss_pct,
        max_drawdown_pct=args.max_drawdown_pct,
        years_tested=args.years_tested,
        num_parameters=args.num_parameters,
        slippage_tested=args.slippage_tested,
        include_india_costs=args.include_india_costs,
        brokerage_per_trade=args.brokerage_per_trade,
        avg_trade_value=args.avg_trade_value,
        trade_type=args.trade_type,
    )

    # Output
    if args.output in ("json", "both"):
        print(json.dumps(result_to_dict(result), indent=2))

    if args.output == "both":
        print("\n" + "=" * 80 + "\n")

    if args.output in ("markdown", "both"):
        print(result_to_markdown(result))

    # Exit code based on verdict
    exit_codes = {"DEPLOY": 0, "REFINE": 1, "REFINE WITH CAUTION": 2, "ABANDON": 3}
    sys.exit(exit_codes.get(result.verdict, 1))


if __name__ == "__main__":
    main()
