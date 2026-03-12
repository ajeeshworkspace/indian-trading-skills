#!/usr/bin/env python3
"""
NSE VCP Screener — Main Orchestrator
Screens Indian stocks (Nifty 50/200/500) for Minervini's Volatility Contraction Pattern.

Usage:
    python3 screen_vcp.py --universe nifty50
    python3 screen_vcp.py --universe nifty500 --output-dir reports/
    python3 screen_vcp.py --custom-tickers RELIANCE,TCS,INFY
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from calculators.trend_template_calculator import calculate_trend_template
from calculators.vcp_pattern_calculator import calculate_vcp
from calculators.volume_pattern_calculator import calculate_volume_pattern
from calculators.pivot_proximity_calculator import calculate_pivot_proximity
from calculators.relative_strength_calculator import calculate_relative_strength
from scorer import calculate_composite_score
from report_generator import generate_reports


def get_universe(universe: str, custom_tickers: str | None = None) -> list[str]:
    """Get stock universe tickers in yfinance format (.NS suffix)."""
    if universe == "custom" and custom_tickers:
        tickers = [t.strip().upper() for t in custom_tickers.split(",")]
        return [f"{t}.NS" for t in tickers if t]

    try:
        from niftystocks import ns

        if universe == "nifty50":
            return ns.get_nifty50_with_ns()
        elif universe == "nifty200":
            return ns.get_nifty200_with_ns()
        elif universe == "nifty500":
            return ns.get_nifty_total_market_with_ns()
        else:
            return ns.get_nifty50_with_ns()
    except ImportError:
        # Fallback: Nifty 50 hardcoded core components
        print("Warning: niftystocks package not available. Using hardcoded Nifty 50 list.", file=sys.stderr)
        nifty50_core = [
            "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
            "BHARTIARTL", "ITC", "SBIN", "LT", "KOTAKBANK",
            "HINDUNILVR", "AXISBANK", "BAJFINANCE", "MARUTI", "TATAMOTORS",
            "SUNPHARMA", "TITAN", "HCLTECH", "NTPC", "POWERGRID",
            "ULTRACEMCO", "ADANIENT", "ASIANPAINT", "TATASTEEL", "WIPRO",
            "ONGC", "JSWSTEEL", "COALINDIA", "NESTLEIND", "BAJAJFINSV",
            "M&M", "TECHM", "DRREDDY", "CIPLA", "EICHERMOT",
            "APOLLOHOSP", "DIVISLAB", "BRITANNIA", "HEROMOTOCO", "INDUSINDBK",
            "TATACONSUM", "HDFCLIFE", "SBILIFE", "BAJAJ-AUTO", "GRASIM",
            "BPCL", "ADANIPORTS", "HINDALCO", "BEL", "TRENT",
        ]
        return [f"{t}.NS" for t in nifty50_core]


def fetch_benchmark(period: str = "1y") -> pd.DataFrame:
    """Fetch Nifty 50 index data as benchmark."""
    try:
        df = yf.download("^NSEI", period=period, interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception as e:
        print(f"Warning: Could not fetch Nifty 50 benchmark: {e}", file=sys.stderr)
        return pd.DataFrame()


def screen_stock(
    ticker: str,
    benchmark_df: pd.DataFrame,
    args: argparse.Namespace,
) -> dict | None:
    """Screen a single stock for VCP pattern. Returns result dict or None."""
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if len(df) < 200:
            return None

        # Check minimum liquidity (₹1 crore daily avg turnover)
        if "Volume" in df.columns and "Close" in df.columns:
            avg_turnover = (df["Volume"].tail(20) * df["Close"].tail(20)).mean()
            if avg_turnover < 1_00_00_000:  # ₹1 crore
                return None

        # Phase 1: Trend Template
        trend = calculate_trend_template(df)
        if trend["score"] < args.trend_min_score:
            return None

        # Phase 2: VCP Detection
        vcp = calculate_vcp(
            df,
            lookback_days=args.lookback_days,
            min_contractions=args.min_contractions,
            t1_depth_min=args.t1_depth_min,
            t1_depth_max=args.t1_depth_max,
            contraction_ratio=args.contraction_ratio,
            min_contraction_days=args.min_contraction_days,
        )

        if not vcp["is_vcp"]:
            return None

        # Phase 3: Scoring
        volume = calculate_volume_pattern(df)
        current_price = float(df["Close"].iloc[-1])
        pivot = vcp["pivot"]
        pivot_prox = calculate_pivot_proximity(current_price, pivot)
        rs = calculate_relative_strength(df, benchmark_df)

        composite = calculate_composite_score(
            trend_score=trend["score"],
            contraction_score=vcp["score"],
            volume_score=volume["score"],
            pivot_score=pivot_prox["score"],
            rs_score=rs["score"],
        )

        clean_ticker = ticker.replace(".NS", "").replace(".BO", "")

        return {
            "ticker": clean_ticker,
            "price": round(current_price, 2),
            "composite_score": composite["composite_score"],
            "quality": composite["quality"],
            "stage": trend["stage"],
            "trend_score": trend["score"],
            "contraction_score": vcp["score"],
            "volume_score": volume["score"],
            "pivot_score": pivot_prox["score"],
            "rs_score": rs["score"],
            "pivot": round(pivot, 2),
            "pivot_distance_pct": pivot_prox["distance_pct"],
            "pivot_position": pivot_prox["position"],
            "dry_up_ratio": volume["dry_up_ratio"],
            "rs_value": rs["rs_value"],
            "contractions": vcp["contractions"],
            "trend_details": trend["details"],
        }

    except Exception as e:
        print(f"  Error screening {ticker}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="NSE VCP Screener")
    parser.add_argument("--universe", default="nifty50",
                        choices=["nifty50", "nifty200", "nifty500", "custom"],
                        help="Stock universe to screen")
    parser.add_argument("--custom-tickers", type=str, default=None,
                        help="Comma-separated tickers for custom universe")
    parser.add_argument("--min-contractions", type=int, default=2,
                        help="Minimum contractions (2-4)")
    parser.add_argument("--t1-depth-min", type=float, default=10.0,
                        help="Minimum T1 depth %%")
    parser.add_argument("--t1-depth-max", type=float, default=40.0,
                        help="Maximum T1 depth %%")
    parser.add_argument("--contraction-ratio", type=float, default=0.75,
                        help="Max contraction ratio")
    parser.add_argument("--min-contraction-days", type=int, default=5,
                        help="Min days per contraction")
    parser.add_argument("--lookback-days", type=int, default=120,
                        help="Pattern lookback days")
    parser.add_argument("--breakout-volume-ratio", type=float, default=1.5,
                        help="Min breakout volume ratio")
    parser.add_argument("--trend-min-score", type=float, default=85.0,
                        help="Min trend template score")
    parser.add_argument("--output-dir", type=str, default="reports",
                        help="Output directory")

    args = parser.parse_args()

    print(f"NSE VCP Screener — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Universe: {args.universe}")

    # Get tickers
    tickers = get_universe(args.universe, args.custom_tickers)
    print(f"Stocks to screen: {len(tickers)}")

    # Fetch benchmark
    print("Fetching Nifty 50 benchmark...")
    benchmark_df = fetch_benchmark()

    # Screen all stocks
    results = []
    total = len(tickers)

    for i, ticker in enumerate(tickers, 1):
        clean = ticker.replace(".NS", "")
        if i % 25 == 0 or i == total:
            print(f"  Progress: {i}/{total} ({clean})")

        result = screen_stock(ticker, benchmark_df, args)
        if result:
            results.append(result)
            print(f"  ✓ VCP found: {clean} (Score: {result['composite_score']:.1f})")

    print(f"\nScreening complete. {len(results)} VCP candidates found.")

    # Generate reports
    if results:
        paths = generate_reports(results, args.output_dir)
        print(f"Reports saved:")
        print(f"  JSON: {paths['json_path']}")
        print(f"  Markdown: {paths['md_path']}")
    else:
        print("No candidates found. Try relaxing parameters or expanding universe.")

    return results


if __name__ == "__main__":
    main()
