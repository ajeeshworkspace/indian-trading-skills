#!/usr/bin/env python3
"""
Black-Scholes Option Pricing Engine for Indian F&O Markets (NSE)

Features:
- European options pricing (NSE options are European-style)
- Full Greeks: Delta, Gamma, Theta, Vega, Rho
- Historical volatility calculation via yfinance
- Multi-leg strategy P/L simulation
- ASCII payoff diagram generation
- CLI interface for standalone use

Default risk-free rate: India 91-day T-bill rate (~6.5-7%)
"""

import argparse
import math
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INDIA_RISK_FREE_RATE = 0.07  # ~7% (91-day T-bill rate approximation)
TRADING_DAYS_PER_YEAR = 252  # NSE trading days per year

# Common NSE F&O lot sizes (reference values — verify via MCP before trading)
DEFAULT_LOT_SIZES = {
    "NIFTY": 75,
    "BANKNIFTY": 15,
    "FINNIFTY": 25,
    "MIDCPNIFTY": 50,
}


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class OptionType(Enum):
    CALL = "CALL"
    PUT = "PUT"


class PositionType(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


# ---------------------------------------------------------------------------
# Math helpers — cumulative normal distribution
# ---------------------------------------------------------------------------

def _norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _norm_cdf(x: float) -> float:
    """
    Cumulative distribution function for the standard normal distribution.
    Uses the Abramowitz and Stegun rational approximation (max error ~7.5e-8).
    """
    if x >= 0:
        return _norm_cdf_positive(x)
    else:
        return 1.0 - _norm_cdf_positive(-x)


def _norm_cdf_positive(x: float) -> float:
    """CDF for x >= 0 using Abramowitz & Stegun approximation 26.2.17."""
    b0 = 0.2316419
    b1 = 0.319381530
    b2 = -0.356563782
    b3 = 1.781477937
    b4 = -1.821255978
    b5 = 1.330274429

    t = 1.0 / (1.0 + b0 * x)
    t2 = t * t
    t3 = t2 * t
    t4 = t3 * t
    t5 = t4 * t

    return 1.0 - _norm_pdf(x) * (b1 * t + b2 * t2 + b3 * t3 + b4 * t4 + b5 * t5)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class OptionLeg:
    """Represents a single option leg in a strategy."""
    option_type: OptionType
    position_type: PositionType
    strike: float
    premium: float
    quantity: int = 1  # Number of lots
    lot_size: int = 1  # Shares per lot

    @property
    def direction(self) -> int:
        """Returns +1 for long, -1 for short."""
        return 1 if self.position_type == PositionType.LONG else -1

    def payoff_at_expiry(self, spot: float) -> float:
        """Calculate payoff per unit at expiry for the given spot price."""
        if self.option_type == OptionType.CALL:
            intrinsic = max(0.0, spot - self.strike)
        else:
            intrinsic = max(0.0, self.strike - spot)

        payoff_per_unit = self.direction * (intrinsic - self.premium)
        return payoff_per_unit * self.quantity * self.lot_size

    def cost(self) -> float:
        """Total cost (debit) or credit of this leg."""
        return -self.direction * self.premium * self.quantity * self.lot_size


@dataclass
class Greeks:
    """Container for option Greeks."""
    delta: float = 0.0
    gamma: float = 0.0
    theta: float = 0.0  # Per calendar day
    vega: float = 0.0   # Per 1% change in volatility
    rho: float = 0.0    # Per 1% change in interest rate


@dataclass
class OptionResult:
    """Result of option pricing calculation."""
    price: float
    greeks: Greeks
    d1: float
    d2: float


@dataclass
class PLPoint:
    """A single point on the P/L curve."""
    spot: float
    pl: float


@dataclass
class StrategyAnalysis:
    """Complete analysis of an options strategy."""
    strategy_name: str
    legs: List[OptionLeg]
    underlying_price: float
    net_premium: float  # Positive = net debit, Negative = net credit
    max_profit: float
    max_loss: float
    breakeven_points: List[float]
    risk_reward_ratio: float
    pl_curve: List[PLPoint]
    net_greeks: Optional[Greeks] = None


# ---------------------------------------------------------------------------
# OptionPricer — Black-Scholes engine
# ---------------------------------------------------------------------------

class OptionPricer:
    """
    Black-Scholes option pricing engine for European options.

    Designed for Indian NSE F&O market where all options are European-style.

    Parameters
    ----------
    spot : float
        Current price of the underlying asset.
    strike : float
        Strike price of the option.
    time_to_expiry : float
        Time to expiry in years. For example, 7 days = 7/365.
    volatility : float
        Annualized volatility as a decimal (e.g., 0.15 for 15%).
    risk_free_rate : float
        Annualized risk-free rate (default: India 91-day T-bill rate).
    dividend_yield : float
        Continuous dividend yield as a decimal (default: 0 for index options).
    """

    def __init__(
        self,
        spot: float,
        strike: float,
        time_to_expiry: float,
        volatility: float,
        risk_free_rate: float = INDIA_RISK_FREE_RATE,
        dividend_yield: float = 0.0,
    ):
        self.S = spot
        self.K = strike
        self.T = max(time_to_expiry, 1e-10)  # Avoid division by zero
        self.sigma = volatility
        self.r = risk_free_rate
        self.q = dividend_yield

        # Pre-calculate d1 and d2
        self._d1, self._d2 = self._calculate_d1_d2()

    def _calculate_d1_d2(self) -> Tuple[float, float]:
        """Calculate the d1 and d2 parameters for Black-Scholes."""
        sqrt_T = math.sqrt(self.T)
        d1 = (
            math.log(self.S / self.K)
            + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T
        ) / (self.sigma * sqrt_T)
        d2 = d1 - self.sigma * sqrt_T
        return d1, d2

    # --- Pricing ---

    def call_price(self) -> float:
        """Calculate the Black-Scholes price of a European call option."""
        return (
            self.S * math.exp(-self.q * self.T) * _norm_cdf(self._d1)
            - self.K * math.exp(-self.r * self.T) * _norm_cdf(self._d2)
        )

    def put_price(self) -> float:
        """Calculate the Black-Scholes price of a European put option."""
        return (
            self.K * math.exp(-self.r * self.T) * _norm_cdf(-self._d2)
            - self.S * math.exp(-self.q * self.T) * _norm_cdf(-self._d1)
        )

    def price(self, option_type: OptionType) -> float:
        """Calculate option price based on type."""
        if option_type == OptionType.CALL:
            return self.call_price()
        else:
            return self.put_price()

    # --- Greeks ---

    def delta(self, option_type: OptionType) -> float:
        """
        Delta: Rate of change of option price with respect to underlying price.
        Call delta: [0, 1], Put delta: [-1, 0]
        """
        eq_discount = math.exp(-self.q * self.T)
        if option_type == OptionType.CALL:
            return eq_discount * _norm_cdf(self._d1)
        else:
            return eq_discount * (_norm_cdf(self._d1) - 1.0)

    def gamma(self) -> float:
        """
        Gamma: Rate of change of delta with respect to underlying price.
        Same for both calls and puts.
        """
        eq_discount = math.exp(-self.q * self.T)
        return (
            eq_discount * _norm_pdf(self._d1)
            / (self.S * self.sigma * math.sqrt(self.T))
        )

    def theta(self, option_type: OptionType) -> float:
        """
        Theta: Rate of change of option price with respect to time.
        Returned as per-calendar-day decay (divide annual by 365).
        Negative for long positions (time decay hurts buyers).
        """
        sqrt_T = math.sqrt(self.T)
        eq_discount = math.exp(-self.q * self.T)

        # Common term
        term1 = -(self.S * eq_discount * _norm_pdf(self._d1) * self.sigma) / (2.0 * sqrt_T)

        if option_type == OptionType.CALL:
            term2 = -self.r * self.K * math.exp(-self.r * self.T) * _norm_cdf(self._d2)
            term3 = self.q * self.S * eq_discount * _norm_cdf(self._d1)
            annual_theta = term1 + term2 + term3
        else:
            term2 = self.r * self.K * math.exp(-self.r * self.T) * _norm_cdf(-self._d2)
            term3 = -self.q * self.S * eq_discount * _norm_cdf(-self._d1)
            annual_theta = term1 + term2 + term3

        return annual_theta / 365.0  # Per calendar day

    def vega(self) -> float:
        """
        Vega: Rate of change of option price with respect to volatility.
        Returned per 1% change in volatility (divide by 100).
        Same for both calls and puts.
        """
        eq_discount = math.exp(-self.q * self.T)
        raw_vega = self.S * eq_discount * _norm_pdf(self._d1) * math.sqrt(self.T)
        return raw_vega / 100.0  # Per 1% vol change

    def rho(self, option_type: OptionType) -> float:
        """
        Rho: Rate of change of option price with respect to interest rate.
        Returned per 1% change in interest rate (divide by 100).
        """
        if option_type == OptionType.CALL:
            raw_rho = (
                self.K * self.T * math.exp(-self.r * self.T) * _norm_cdf(self._d2)
            )
        else:
            raw_rho = (
                -self.K * self.T * math.exp(-self.r * self.T) * _norm_cdf(-self._d2)
            )
        return raw_rho / 100.0  # Per 1% rate change

    def all_greeks(self, option_type: OptionType) -> Greeks:
        """Calculate all Greeks for the given option type."""
        return Greeks(
            delta=self.delta(option_type),
            gamma=self.gamma(),
            theta=self.theta(option_type),
            vega=self.vega(),
            rho=self.rho(option_type),
        )

    def full_result(self, option_type: OptionType) -> OptionResult:
        """Return complete pricing result with price, Greeks, and intermediates."""
        return OptionResult(
            price=self.price(option_type),
            greeks=self.all_greeks(option_type),
            d1=self._d1,
            d2=self._d2,
        )

    # --- Implied Volatility ---

    @staticmethod
    def implied_volatility(
        market_price: float,
        spot: float,
        strike: float,
        time_to_expiry: float,
        option_type: OptionType,
        risk_free_rate: float = INDIA_RISK_FREE_RATE,
        dividend_yield: float = 0.0,
        tolerance: float = 1e-6,
        max_iterations: int = 100,
    ) -> float:
        """
        Calculate implied volatility using the Newton-Raphson method.

        Parameters
        ----------
        market_price : float
            The observed market price of the option.
        spot, strike, time_to_expiry : float
            Option parameters.
        option_type : OptionType
            CALL or PUT.
        risk_free_rate, dividend_yield : float
            Market parameters.
        tolerance : float
            Convergence tolerance.
        max_iterations : int
            Maximum iterations for Newton-Raphson.

        Returns
        -------
        float
            Implied volatility as a decimal.

        Raises
        ------
        ValueError
            If the method does not converge.
        """
        # Initial guess using Brenner-Subrahmanyam approximation
        sigma = math.sqrt(2.0 * math.pi / time_to_expiry) * (market_price / spot)
        sigma = max(sigma, 0.01)  # Floor at 1%

        for i in range(max_iterations):
            pricer = OptionPricer(
                spot, strike, time_to_expiry, sigma, risk_free_rate, dividend_yield
            )
            price = pricer.price(option_type)
            vega_raw = pricer.vega() * 100.0  # Convert back to raw vega

            if abs(vega_raw) < 1e-12:
                # Vega too small — bisection fallback
                break

            diff = price - market_price

            if abs(diff) < tolerance:
                return sigma

            sigma = sigma - diff / vega_raw
            sigma = max(sigma, 0.001)  # Prevent negative volatility

        # Bisection fallback if Newton-Raphson didn't converge
        return OptionPricer._iv_bisection(
            market_price, spot, strike, time_to_expiry, option_type,
            risk_free_rate, dividend_yield, tolerance, max_iterations
        )

    @staticmethod
    def _iv_bisection(
        market_price: float,
        spot: float,
        strike: float,
        time_to_expiry: float,
        option_type: OptionType,
        risk_free_rate: float,
        dividend_yield: float,
        tolerance: float,
        max_iterations: int,
    ) -> float:
        """Bisection method fallback for implied volatility."""
        low = 0.001
        high = 5.0  # 500% volatility upper bound

        for _ in range(max_iterations):
            mid = (low + high) / 2.0
            pricer = OptionPricer(
                spot, strike, time_to_expiry, mid, risk_free_rate, dividend_yield
            )
            price = pricer.price(option_type)
            diff = price - market_price

            if abs(diff) < tolerance:
                return mid

            if diff > 0:
                high = mid
            else:
                low = mid

        raise ValueError(
            f"Implied volatility did not converge after {max_iterations} iterations. "
            f"Market price: {market_price}, Spot: {spot}, Strike: {strike}, "
            f"T: {time_to_expiry}, Type: {option_type.value}"
        )


# ---------------------------------------------------------------------------
# Historical Volatility Calculator
# ---------------------------------------------------------------------------

def calculate_historical_volatility(
    ticker: str,
    days: int = 30,
    annualize: bool = True,
) -> float:
    """
    Calculate historical volatility from daily returns using yfinance data.

    Parameters
    ----------
    ticker : str
        Yahoo Finance ticker symbol. For Indian stocks use ".NS" suffix
        (e.g., "RELIANCE.NS", "^NSEI" for Nifty, "^NSEBANK" for Bank Nifty).
    days : int
        Number of trading days to look back (default: 30).
    annualize : bool
        If True, annualize the volatility (multiply by sqrt(252)).

    Returns
    -------
    float
        Historical volatility as a decimal.
    """
    try:
        import yfinance as yf
    except ImportError:
        print(
            "ERROR: yfinance is not installed. Install it with: pip install yfinance",
            file=sys.stderr,
        )
        print(
            "Returning default volatility of 15% as fallback.",
            file=sys.stderr,
        )
        return 0.15

    # Map common Indian index names to Yahoo Finance tickers
    ticker_map = {
        "NIFTY": "^NSEI",
        "NIFTY50": "^NSEI",
        "BANKNIFTY": "^NSEBANK",
        "NIFTYBANK": "^NSEBANK",
        "FINNIFTY": "NIFTY_FIN_SERVICE.NS",
        "INDIAVIX": "^INDIAVIX",
        "SENSEX": "^BSESN",
    }

    yf_ticker = ticker_map.get(ticker.upper(), ticker)

    # Add .NS suffix for Indian stocks if not already present
    if (
        not yf_ticker.startswith("^")
        and not yf_ticker.endswith(".NS")
        and not yf_ticker.endswith(".BO")
    ):
        yf_ticker = yf_ticker + ".NS"

    # Fetch extra days to account for weekends and holidays
    fetch_days = int(days * 1.6) + 10

    try:
        data = yf.download(
            yf_ticker,
            period=f"{fetch_days}d",
            progress=False,
            auto_adjust=True,
        )

        if data.empty or len(data) < 5:
            print(
                f"WARNING: Insufficient data for {yf_ticker}. "
                f"Returning default volatility of 15%.",
                file=sys.stderr,
            )
            return 0.15

        # Use closing prices
        closes = data["Close"].dropna().values.flatten()
        if len(closes) < 2:
            return 0.15

        # Take the most recent 'days' trading days
        closes = closes[-(days + 1):]

        # Calculate log returns
        log_returns = []
        for i in range(1, len(closes)):
            if closes[i - 1] > 0 and closes[i] > 0:
                log_returns.append(math.log(closes[i] / closes[i - 1]))

        if len(log_returns) < 2:
            return 0.15

        # Standard deviation of log returns
        mean_return = sum(log_returns) / len(log_returns)
        variance = sum((r - mean_return) ** 2 for r in log_returns) / (len(log_returns) - 1)
        daily_vol = math.sqrt(variance)

        if annualize:
            return daily_vol * math.sqrt(TRADING_DAYS_PER_YEAR)
        else:
            return daily_vol

    except Exception as e:
        print(
            f"WARNING: Could not fetch data for {yf_ticker}: {e}. "
            f"Returning default volatility of 15%.",
            file=sys.stderr,
        )
        return 0.15


# ---------------------------------------------------------------------------
# P/L Simulation
# ---------------------------------------------------------------------------

def simulate_pl(
    strategy_legs: List[OptionLeg],
    price_range: Tuple[float, float],
    num_points: int = 50,
) -> List[PLPoint]:
    """
    Simulate profit/loss at expiry across a range of underlying prices.

    Parameters
    ----------
    strategy_legs : list of OptionLeg
        The legs of the options strategy.
    price_range : tuple of (float, float)
        (min_price, max_price) for simulation.
    num_points : int
        Number of price points to simulate.

    Returns
    -------
    list of PLPoint
        P/L at each price point.
    """
    min_price, max_price = price_range
    step = (max_price - min_price) / max(num_points - 1, 1)
    pl_curve = []

    for i in range(num_points):
        spot = min_price + i * step
        total_pl = sum(leg.payoff_at_expiry(spot) for leg in strategy_legs)
        pl_curve.append(PLPoint(spot=round(spot, 2), pl=round(total_pl, 2)))

    return pl_curve


def find_breakeven_points(
    strategy_legs: List[OptionLeg],
    price_range: Tuple[float, float],
    num_points: int = 1000,
) -> List[float]:
    """
    Find breakeven points where P/L crosses zero.

    Uses linear interpolation between simulated points.
    """
    pl_curve = simulate_pl(strategy_legs, price_range, num_points)
    breakevens = []

    for i in range(1, len(pl_curve)):
        prev = pl_curve[i - 1]
        curr = pl_curve[i]

        # Check for sign change
        if prev.pl * curr.pl < 0:
            # Linear interpolation
            if abs(curr.pl - prev.pl) > 1e-10:
                ratio = abs(prev.pl) / abs(curr.pl - prev.pl)
                be_price = prev.spot + ratio * (curr.spot - prev.spot)
                breakevens.append(round(be_price, 2))
        elif abs(curr.pl) < 0.01:
            breakevens.append(curr.spot)

    return breakevens


def analyze_strategy(
    strategy_name: str,
    legs: List[OptionLeg],
    underlying_price: float,
    price_range: Optional[Tuple[float, float]] = None,
    num_points: int = 50,
    net_greeks: Optional[Greeks] = None,
) -> StrategyAnalysis:
    """
    Perform complete analysis of an options strategy.

    Parameters
    ----------
    strategy_name : str
        Name of the strategy (e.g., "Iron Condor").
    legs : list of OptionLeg
        All legs of the strategy.
    underlying_price : float
        Current price of the underlying.
    price_range : tuple of (float, float), optional
        Price range for simulation. Defaults to +/- 10% of underlying.
    num_points : int
        Number of simulation points.
    net_greeks : Greeks, optional
        Pre-calculated net Greeks for the position.

    Returns
    -------
    StrategyAnalysis
        Complete strategy analysis.
    """
    if price_range is None:
        margin = underlying_price * 0.10
        price_range = (underlying_price - margin, underlying_price + margin)

    # Net premium
    net_premium = sum(
        leg.direction * leg.premium * leg.quantity * leg.lot_size
        for leg in legs
    )

    # P/L curve
    pl_curve = simulate_pl(legs, price_range, num_points)

    # Max profit and max loss
    max_profit = max(point.pl for point in pl_curve)
    max_loss = min(point.pl for point in pl_curve)

    # Breakeven points
    breakevens = find_breakeven_points(legs, price_range, num_points=1000)

    # Risk-reward ratio
    if abs(max_loss) > 1e-10:
        risk_reward = abs(max_profit / max_loss)
    else:
        risk_reward = float("inf")

    return StrategyAnalysis(
        strategy_name=strategy_name,
        legs=legs,
        underlying_price=underlying_price,
        net_premium=net_premium,
        max_profit=max_profit,
        max_loss=max_loss,
        breakeven_points=breakevens,
        risk_reward_ratio=round(risk_reward, 2),
        pl_curve=pl_curve,
        net_greeks=net_greeks,
    )


# ---------------------------------------------------------------------------
# ASCII P/L Diagram Generator
# ---------------------------------------------------------------------------

def generate_ascii_pl_diagram(
    pl_data: List[PLPoint],
    width: int = 60,
    height: int = 20,
    title: str = "P/L at Expiry",
) -> str:
    """
    Generate an ASCII art P/L diagram.

    Parameters
    ----------
    pl_data : list of PLPoint
        P/L data points to plot.
    width : int
        Width of the chart in characters.
    height : int
        Height of the chart in characters.
    title : str
        Title to display above the chart.

    Returns
    -------
    str
        ASCII art P/L diagram as a multi-line string.
    """
    if not pl_data:
        return "No data to plot."

    spots = [p.spot for p in pl_data]
    pls = [p.pl for p in pl_data]

    min_spot = min(spots)
    max_spot = max(spots)
    min_pl = min(pls)
    max_pl = max(pls)

    # Add padding to P/L range
    pl_range = max_pl - min_pl
    if pl_range < 1e-10:
        pl_range = 1.0
        min_pl -= 0.5
        max_pl += 0.5

    spot_range = max_spot - min_spot
    if spot_range < 1e-10:
        spot_range = 1.0

    # Determine zero line position
    if min_pl <= 0 <= max_pl:
        zero_row = height - 1 - int((0 - min_pl) / pl_range * (height - 1))
    else:
        zero_row = -1  # Zero line is outside the chart

    # Build the grid
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Draw zero line
    if 0 <= zero_row < height:
        for c in range(width):
            grid[zero_row][c] = "-"

    # Plot the P/L curve
    for point in pl_data:
        col = int((point.spot - min_spot) / spot_range * (width - 1))
        row = height - 1 - int((point.pl - min_pl) / pl_range * (height - 1))
        col = max(0, min(col, width - 1))
        row = max(0, min(row, height - 1))

        if point.pl > 0:
            grid[row][col] = "+"
        elif point.pl < 0:
            grid[row][col] = "o"
        else:
            grid[row][col] = "*"

    # Build output
    lines = []
    lines.append("")
    lines.append(f"  {title}")
    lines.append(f"  {'=' * (width + 12)}")

    # Y-axis labels
    for r in range(height):
        pl_value = max_pl - (r / (height - 1)) * pl_range
        label = f"{pl_value:>10.0f}"
        row_str = "".join(grid[r])

        if r == zero_row:
            lines.append(f"{label} |{row_str}|  <- Zero")
        else:
            lines.append(f"{label} |{row_str}|")

    # X-axis
    lines.append(f"{'':>10} +{'=' * width}+")

    # X-axis labels
    x_label_positions = [0, width // 4, width // 2, 3 * width // 4, width - 1]
    x_labels = []
    for pos in x_label_positions:
        spot_value = min_spot + (pos / (width - 1)) * spot_range
        x_labels.append(f"{spot_value:.0f}")

    # Distribute labels across the x-axis
    x_label_line = " " * 11
    positions_used = 0
    for i, pos in enumerate(x_label_positions):
        label = x_labels[i]
        actual_pos = 11 + pos
        padding = actual_pos - len(x_label_line)
        if padding > 0:
            x_label_line += " " * padding
        x_label_line += label
    lines.append(x_label_line)

    # Legend
    lines.append("")
    lines.append(f"  Legend: '+' = Profit | 'o' = Loss | '*' = Breakeven | '-' = Zero line")
    lines.append(f"  X-axis: Underlying price at expiry")
    lines.append(f"  Y-axis: Profit / Loss")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Strategy Report Generator
# ---------------------------------------------------------------------------

def generate_strategy_report(analysis: StrategyAnalysis) -> str:
    """Generate a formatted text report of the strategy analysis."""
    lines = []
    lines.append("")
    lines.append("=" * 70)
    lines.append("  OPTIONS STRATEGY REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  Strategy     : {analysis.strategy_name}")
    lines.append(f"  Underlying   : {analysis.underlying_price:.2f}")
    lines.append("")

    # Legs
    lines.append("-" * 70)
    lines.append("  STRATEGY LEGS")
    lines.append("-" * 70)
    for i, leg in enumerate(analysis.legs, 1):
        direction_str = "BUY" if leg.position_type == PositionType.LONG else "SELL"
        lines.append(
            f"  Leg {i}: {direction_str:4s} {leg.quantity} x "
            f"{leg.option_type.value:4s} @ Strike {leg.strike:.2f} "
            f"for {leg.premium:.2f} "
            f"(Lot size: {leg.lot_size})"
        )
    lines.append("")

    # Key Metrics
    lines.append("-" * 70)
    lines.append("  KEY METRICS")
    lines.append("-" * 70)

    premium_type = "DEBIT" if analysis.net_premium > 0 else "CREDIT"
    lines.append(
        f"  Net Premium     : {premium_type} {abs(analysis.net_premium):.2f}"
    )
    lines.append(f"  Max Profit      : {analysis.max_profit:.2f}")
    lines.append(f"  Max Loss        : {analysis.max_loss:.2f}")

    if analysis.breakeven_points:
        be_str = ", ".join(f"{be:.2f}" for be in analysis.breakeven_points)
        lines.append(f"  Breakeven(s)    : {be_str}")
    else:
        lines.append(f"  Breakeven(s)    : None found in range")

    lines.append(f"  Risk-Reward     : 1:{analysis.risk_reward_ratio:.2f}")
    lines.append("")

    # Net Greeks
    if analysis.net_greeks:
        lines.append("-" * 70)
        lines.append("  NET POSITION GREEKS")
        lines.append("-" * 70)
        g = analysis.net_greeks
        lines.append(f"  Delta : {g.delta:>10.4f}")
        lines.append(f"  Gamma : {g.gamma:>10.6f}")
        lines.append(f"  Theta : {g.theta:>10.4f}  (per day)")
        lines.append(f"  Vega  : {g.vega:>10.4f}  (per 1% IV change)")
        lines.append(f"  Rho   : {g.rho:>10.4f}  (per 1% rate change)")
        lines.append("")

    # P/L Diagram
    if analysis.pl_curve:
        diagram = generate_ascii_pl_diagram(
            analysis.pl_curve, title=f"P/L Diagram: {analysis.strategy_name}"
        )
        lines.append("-" * 70)
        lines.append("  PAYOFF DIAGRAM")
        lines.append("-" * 70)
        lines.append(diagram)
        lines.append("")

    # Risk Management
    lines.append("-" * 70)
    lines.append("  RISK MANAGEMENT NOTES")
    lines.append("-" * 70)
    lines.append("  - Set stop-loss if unrealized loss exceeds 2x premium received")
    lines.append("  - Monitor margin requirements daily (SEBI peak margin rules)")
    lines.append("  - Watch for F&O ban risk if stock OI approaches 95% MWPL")
    lines.append("  - Close ITM options before expiry to avoid STT on exercise")
    lines.append("  - For stock options: physical settlement requires delivery margin")
    lines.append("  - Review position 2-3 days before expiry for rollover decision")
    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Pre-built Strategy Constructors
# ---------------------------------------------------------------------------

def build_bull_call_spread(
    lower_strike: float,
    upper_strike: float,
    lower_premium: float,
    upper_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Bull Call Spread: Buy lower strike call, sell upper strike call."""
    return [
        OptionLeg(OptionType.CALL, PositionType.LONG, lower_strike, lower_premium, lots, lot_size),
        OptionLeg(OptionType.CALL, PositionType.SHORT, upper_strike, upper_premium, lots, lot_size),
    ]


def build_bear_put_spread(
    upper_strike: float,
    lower_strike: float,
    upper_premium: float,
    lower_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Bear Put Spread: Buy higher strike put, sell lower strike put."""
    return [
        OptionLeg(OptionType.PUT, PositionType.LONG, upper_strike, upper_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.SHORT, lower_strike, lower_premium, lots, lot_size),
    ]


def build_bull_put_spread(
    upper_strike: float,
    lower_strike: float,
    upper_premium: float,
    lower_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Bull Put Spread: Sell higher strike put, buy lower strike put."""
    return [
        OptionLeg(OptionType.PUT, PositionType.SHORT, upper_strike, upper_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.LONG, lower_strike, lower_premium, lots, lot_size),
    ]


def build_bear_call_spread(
    lower_strike: float,
    upper_strike: float,
    lower_premium: float,
    upper_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Bear Call Spread: Sell lower strike call, buy upper strike call."""
    return [
        OptionLeg(OptionType.CALL, PositionType.SHORT, lower_strike, lower_premium, lots, lot_size),
        OptionLeg(OptionType.CALL, PositionType.LONG, upper_strike, upper_premium, lots, lot_size),
    ]


def build_long_straddle(
    strike: float,
    call_premium: float,
    put_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Long Straddle: Buy ATM call and ATM put at same strike."""
    return [
        OptionLeg(OptionType.CALL, PositionType.LONG, strike, call_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.LONG, strike, put_premium, lots, lot_size),
    ]


def build_short_straddle(
    strike: float,
    call_premium: float,
    put_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Short Straddle: Sell ATM call and ATM put at same strike."""
    return [
        OptionLeg(OptionType.CALL, PositionType.SHORT, strike, call_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.SHORT, strike, put_premium, lots, lot_size),
    ]


def build_long_strangle(
    call_strike: float,
    put_strike: float,
    call_premium: float,
    put_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Long Strangle: Buy OTM call and OTM put."""
    return [
        OptionLeg(OptionType.CALL, PositionType.LONG, call_strike, call_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.LONG, put_strike, put_premium, lots, lot_size),
    ]


def build_short_strangle(
    call_strike: float,
    put_strike: float,
    call_premium: float,
    put_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """Build a Short Strangle: Sell OTM call and OTM put."""
    return [
        OptionLeg(OptionType.CALL, PositionType.SHORT, call_strike, call_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.SHORT, put_strike, put_premium, lots, lot_size),
    ]


def build_iron_condor(
    put_buy_strike: float,
    put_sell_strike: float,
    call_sell_strike: float,
    call_buy_strike: float,
    put_buy_premium: float,
    put_sell_premium: float,
    call_sell_premium: float,
    call_buy_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """
    Build an Iron Condor:
    Buy OTM Put (lowest) + Sell Put (lower-mid) + Sell Call (upper-mid) + Buy OTM Call (highest).
    """
    return [
        OptionLeg(OptionType.PUT, PositionType.LONG, put_buy_strike, put_buy_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.SHORT, put_sell_strike, put_sell_premium, lots, lot_size),
        OptionLeg(OptionType.CALL, PositionType.SHORT, call_sell_strike, call_sell_premium, lots, lot_size),
        OptionLeg(OptionType.CALL, PositionType.LONG, call_buy_strike, call_buy_premium, lots, lot_size),
    ]


def build_iron_butterfly(
    put_buy_strike: float,
    atm_strike: float,
    call_buy_strike: float,
    put_buy_premium: float,
    atm_put_premium: float,
    atm_call_premium: float,
    call_buy_premium: float,
    lots: int = 1,
    lot_size: int = 75,
) -> List[OptionLeg]:
    """
    Build an Iron Butterfly:
    Buy OTM Put + Sell ATM Put + Sell ATM Call + Buy OTM Call.
    """
    return [
        OptionLeg(OptionType.PUT, PositionType.LONG, put_buy_strike, put_buy_premium, lots, lot_size),
        OptionLeg(OptionType.PUT, PositionType.SHORT, atm_strike, atm_put_premium, lots, lot_size),
        OptionLeg(OptionType.CALL, PositionType.SHORT, atm_strike, atm_call_premium, lots, lot_size),
        OptionLeg(OptionType.CALL, PositionType.LONG, call_buy_strike, call_buy_premium, lots, lot_size),
    ]


# ---------------------------------------------------------------------------
# Command-Line Interface
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Black-Scholes Option Pricing Engine for Indian F&O Markets (NSE)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Price a NIFTY call option
  python black_scholes.py price --spot 24000 --strike 24500 --expiry-days 7 --vol 0.13 --type CALL

  # Calculate all Greeks
  python black_scholes.py greeks --spot 24000 --strike 24500 --expiry-days 7 --vol 0.13 --type CALL

  # Calculate implied volatility from market price
  python black_scholes.py iv --spot 24000 --strike 24500 --expiry-days 7 --market-price 120 --type CALL

  # Calculate historical volatility for NIFTY
  python black_scholes.py hvol --ticker NIFTY --days 30

  # Analyze a Bull Call Spread
  python black_scholes.py strategy --type bull-call-spread \\
      --spot 24000 --lower-strike 24000 --upper-strike 24500 \\
      --lower-premium 250 --upper-premium 80 --lot-size 75

  # Analyze a Short Straddle
  python black_scholes.py strategy --type short-straddle \\
      --spot 24000 --atm-strike 24000 \\
      --call-premium 200 --put-premium 180 --lot-size 75

  # Analyze an Iron Condor
  python black_scholes.py strategy --type iron-condor \\
      --spot 24000 --lot-size 75 \\
      --put-buy-strike 23500 --put-sell-strike 23800 \\
      --call-sell-strike 24200 --call-buy-strike 24500 \\
      --put-buy-premium 30 --put-sell-premium 70 \\
      --call-sell-premium 65 --call-buy-premium 25
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # --- Price command ---
    price_parser = subparsers.add_parser("price", help="Calculate option price")
    price_parser.add_argument("--spot", type=float, required=True, help="Underlying spot price")
    price_parser.add_argument("--strike", type=float, required=True, help="Strike price")
    price_parser.add_argument("--expiry-days", type=float, required=True, help="Days to expiry")
    price_parser.add_argument("--vol", type=float, required=True, help="Annualized volatility (decimal, e.g., 0.15)")
    price_parser.add_argument("--type", choices=["CALL", "PUT"], required=True, help="Option type")
    price_parser.add_argument("--rate", type=float, default=INDIA_RISK_FREE_RATE, help=f"Risk-free rate (default: {INDIA_RISK_FREE_RATE})")
    price_parser.add_argument("--div-yield", type=float, default=0.0, help="Dividend yield (default: 0)")

    # --- Greeks command ---
    greeks_parser = subparsers.add_parser("greeks", help="Calculate all Greeks")
    greeks_parser.add_argument("--spot", type=float, required=True, help="Underlying spot price")
    greeks_parser.add_argument("--strike", type=float, required=True, help="Strike price")
    greeks_parser.add_argument("--expiry-days", type=float, required=True, help="Days to expiry")
    greeks_parser.add_argument("--vol", type=float, required=True, help="Annualized volatility (decimal)")
    greeks_parser.add_argument("--type", choices=["CALL", "PUT"], required=True, help="Option type")
    greeks_parser.add_argument("--rate", type=float, default=INDIA_RISK_FREE_RATE, help=f"Risk-free rate (default: {INDIA_RISK_FREE_RATE})")
    greeks_parser.add_argument("--div-yield", type=float, default=0.0, help="Dividend yield (default: 0)")

    # --- Implied Volatility command ---
    iv_parser = subparsers.add_parser("iv", help="Calculate implied volatility")
    iv_parser.add_argument("--spot", type=float, required=True, help="Underlying spot price")
    iv_parser.add_argument("--strike", type=float, required=True, help="Strike price")
    iv_parser.add_argument("--expiry-days", type=float, required=True, help="Days to expiry")
    iv_parser.add_argument("--market-price", type=float, required=True, help="Observed market price of the option")
    iv_parser.add_argument("--type", choices=["CALL", "PUT"], required=True, help="Option type")
    iv_parser.add_argument("--rate", type=float, default=INDIA_RISK_FREE_RATE, help=f"Risk-free rate (default: {INDIA_RISK_FREE_RATE})")
    iv_parser.add_argument("--div-yield", type=float, default=0.0, help="Dividend yield (default: 0)")

    # --- Historical Volatility command ---
    hvol_parser = subparsers.add_parser("hvol", help="Calculate historical volatility")
    hvol_parser.add_argument("--ticker", type=str, required=True, help="Ticker symbol (e.g., NIFTY, RELIANCE, TCS)")
    hvol_parser.add_argument("--days", type=int, default=30, help="Lookback period in trading days (default: 30)")

    # --- Strategy command ---
    strat_parser = subparsers.add_parser("strategy", help="Analyze an options strategy")
    strat_parser.add_argument(
        "--type",
        choices=[
            "bull-call-spread", "bear-put-spread", "bull-put-spread", "bear-call-spread",
            "long-straddle", "short-straddle", "long-strangle", "short-strangle",
            "iron-condor", "iron-butterfly",
        ],
        required=True,
        help="Strategy type",
    )
    strat_parser.add_argument("--spot", type=float, required=True, help="Underlying spot price")
    strat_parser.add_argument("--lot-size", type=int, default=75, help="Lot size (default: 75 for NIFTY)")
    strat_parser.add_argument("--lots", type=int, default=1, help="Number of lots (default: 1)")

    # Strike arguments for various strategies
    strat_parser.add_argument("--lower-strike", type=float, help="Lower strike price")
    strat_parser.add_argument("--upper-strike", type=float, help="Upper strike price")
    strat_parser.add_argument("--atm-strike", type=float, help="ATM strike price")
    strat_parser.add_argument("--call-strike", type=float, help="Call strike (for strangles)")
    strat_parser.add_argument("--put-strike", type=float, help="Put strike (for strangles)")
    strat_parser.add_argument("--put-buy-strike", type=float, help="Put buy strike (for iron condor/butterfly)")
    strat_parser.add_argument("--put-sell-strike", type=float, help="Put sell strike (for iron condor)")
    strat_parser.add_argument("--call-sell-strike", type=float, help="Call sell strike (for iron condor)")
    strat_parser.add_argument("--call-buy-strike", type=float, help="Call buy strike (for iron condor/butterfly)")

    # Premium arguments
    strat_parser.add_argument("--lower-premium", type=float, help="Lower strike premium")
    strat_parser.add_argument("--upper-premium", type=float, help="Upper strike premium")
    strat_parser.add_argument("--call-premium", type=float, help="Call premium")
    strat_parser.add_argument("--put-premium", type=float, help="Put premium")
    strat_parser.add_argument("--put-buy-premium", type=float, help="Put buy premium (iron condor/butterfly)")
    strat_parser.add_argument("--put-sell-premium", type=float, help="Put sell premium (iron condor)")
    strat_parser.add_argument("--call-sell-premium", type=float, help="Call sell premium (iron condor)")
    strat_parser.add_argument("--call-buy-premium", type=float, help="Call buy premium (iron condor/butterfly)")
    strat_parser.add_argument("--atm-call-premium", type=float, help="ATM call premium (iron butterfly)")
    strat_parser.add_argument("--atm-put-premium", type=float, help="ATM put premium (iron butterfly)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # --- Execute commands ---

    if args.command == "price":
        opt_type = OptionType.CALL if args.type == "CALL" else OptionType.PUT
        pricer = OptionPricer(
            spot=args.spot,
            strike=args.strike,
            time_to_expiry=args.expiry_days / 365.0,
            volatility=args.vol,
            risk_free_rate=args.rate,
            dividend_yield=args.div_yield,
        )
        price = pricer.price(opt_type)
        print(f"\n{'=' * 50}")
        print(f"  Black-Scholes Option Price")
        print(f"{'=' * 50}")
        print(f"  Underlying  : {args.spot:.2f}")
        print(f"  Strike      : {args.strike:.2f}")
        print(f"  Days to Exp : {args.expiry_days:.0f}")
        print(f"  Volatility  : {args.vol:.2%}")
        print(f"  Risk-Free   : {args.rate:.2%}")
        print(f"  Type        : {args.type}")
        print(f"  ---------------------")
        print(f"  PRICE       : {price:.2f}")
        print(f"{'=' * 50}\n")

    elif args.command == "greeks":
        opt_type = OptionType.CALL if args.type == "CALL" else OptionType.PUT
        pricer = OptionPricer(
            spot=args.spot,
            strike=args.strike,
            time_to_expiry=args.expiry_days / 365.0,
            volatility=args.vol,
            risk_free_rate=args.rate,
            dividend_yield=args.div_yield,
        )
        result = pricer.full_result(opt_type)
        print(f"\n{'=' * 50}")
        print(f"  Black-Scholes Greeks")
        print(f"{'=' * 50}")
        print(f"  Underlying  : {args.spot:.2f}")
        print(f"  Strike      : {args.strike:.2f}")
        print(f"  Days to Exp : {args.expiry_days:.0f}")
        print(f"  Volatility  : {args.vol:.2%}")
        print(f"  Risk-Free   : {args.rate:.2%}")
        print(f"  Type        : {args.type}")
        print(f"  ---------------------")
        print(f"  Price       : {result.price:.4f}")
        print(f"  Delta       : {result.greeks.delta:.6f}")
        print(f"  Gamma       : {result.greeks.gamma:.6f}")
        print(f"  Theta       : {result.greeks.theta:.4f}  (per day)")
        print(f"  Vega        : {result.greeks.vega:.4f}  (per 1% vol)")
        print(f"  Rho         : {result.greeks.rho:.4f}  (per 1% rate)")
        print(f"  d1          : {result.d1:.6f}")
        print(f"  d2          : {result.d2:.6f}")
        print(f"{'=' * 50}\n")

    elif args.command == "iv":
        opt_type = OptionType.CALL if args.type == "CALL" else OptionType.PUT
        try:
            iv = OptionPricer.implied_volatility(
                market_price=args.market_price,
                spot=args.spot,
                strike=args.strike,
                time_to_expiry=args.expiry_days / 365.0,
                option_type=opt_type,
                risk_free_rate=args.rate,
                dividend_yield=args.div_yield,
            )
            print(f"\n{'=' * 50}")
            print(f"  Implied Volatility")
            print(f"{'=' * 50}")
            print(f"  Underlying    : {args.spot:.2f}")
            print(f"  Strike        : {args.strike:.2f}")
            print(f"  Days to Exp   : {args.expiry_days:.0f}")
            print(f"  Market Price  : {args.market_price:.2f}")
            print(f"  Type          : {args.type}")
            print(f"  ---------------------")
            print(f"  IMPLIED VOL   : {iv:.4f} ({iv:.2%})")
            print(f"{'=' * 50}\n")
        except ValueError as e:
            print(f"\nERROR: {e}\n", file=sys.stderr)
            sys.exit(1)

    elif args.command == "hvol":
        hvol = calculate_historical_volatility(args.ticker, args.days)
        print(f"\n{'=' * 50}")
        print(f"  Historical Volatility")
        print(f"{'=' * 50}")
        print(f"  Ticker        : {args.ticker}")
        print(f"  Lookback      : {args.days} trading days")
        print(f"  ---------------------")
        print(f"  HIST VOL      : {hvol:.4f} ({hvol:.2%})")
        print(f"{'=' * 50}\n")

    elif args.command == "strategy":
        legs = _build_strategy_from_args(args)
        if legs is None:
            sys.exit(1)

        strategy_name = args.type.replace("-", " ").title()
        analysis = analyze_strategy(
            strategy_name=strategy_name,
            legs=legs,
            underlying_price=args.spot,
        )
        report = generate_strategy_report(analysis)
        print(report)


def _build_strategy_from_args(args) -> Optional[List[OptionLeg]]:
    """Build strategy legs from CLI arguments."""
    lot_size = args.lot_size
    lots = args.lots

    if args.type == "bull-call-spread":
        if not all([args.lower_strike, args.upper_strike, args.lower_premium, args.upper_premium]):
            print("ERROR: Bull Call Spread requires --lower-strike, --upper-strike, --lower-premium, --upper-premium", file=sys.stderr)
            return None
        return build_bull_call_spread(
            args.lower_strike, args.upper_strike,
            args.lower_premium, args.upper_premium,
            lots, lot_size,
        )

    elif args.type == "bear-put-spread":
        if not all([args.upper_strike, args.lower_strike, args.upper_premium, args.lower_premium]):
            print("ERROR: Bear Put Spread requires --upper-strike, --lower-strike, --upper-premium, --lower-premium", file=sys.stderr)
            return None
        return build_bear_put_spread(
            args.upper_strike, args.lower_strike,
            args.upper_premium, args.lower_premium,
            lots, lot_size,
        )

    elif args.type == "bull-put-spread":
        if not all([args.upper_strike, args.lower_strike, args.upper_premium, args.lower_premium]):
            print("ERROR: Bull Put Spread requires --upper-strike, --lower-strike, --upper-premium, --lower-premium", file=sys.stderr)
            return None
        return build_bull_put_spread(
            args.upper_strike, args.lower_strike,
            args.upper_premium, args.lower_premium,
            lots, lot_size,
        )

    elif args.type == "bear-call-spread":
        if not all([args.lower_strike, args.upper_strike, args.lower_premium, args.upper_premium]):
            print("ERROR: Bear Call Spread requires --lower-strike, --upper-strike, --lower-premium, --upper-premium", file=sys.stderr)
            return None
        return build_bear_call_spread(
            args.lower_strike, args.upper_strike,
            args.lower_premium, args.upper_premium,
            lots, lot_size,
        )

    elif args.type == "long-straddle":
        if not all([args.atm_strike, args.call_premium, args.put_premium]):
            print("ERROR: Long Straddle requires --atm-strike, --call-premium, --put-premium", file=sys.stderr)
            return None
        return build_long_straddle(
            args.atm_strike, args.call_premium, args.put_premium,
            lots, lot_size,
        )

    elif args.type == "short-straddle":
        if not all([args.atm_strike, args.call_premium, args.put_premium]):
            print("ERROR: Short Straddle requires --atm-strike, --call-premium, --put-premium", file=sys.stderr)
            return None
        return build_short_straddle(
            args.atm_strike, args.call_premium, args.put_premium,
            lots, lot_size,
        )

    elif args.type == "long-strangle":
        if not all([args.call_strike, args.put_strike, args.call_premium, args.put_premium]):
            print("ERROR: Long Strangle requires --call-strike, --put-strike, --call-premium, --put-premium", file=sys.stderr)
            return None
        return build_long_strangle(
            args.call_strike, args.put_strike,
            args.call_premium, args.put_premium,
            lots, lot_size,
        )

    elif args.type == "short-strangle":
        if not all([args.call_strike, args.put_strike, args.call_premium, args.put_premium]):
            print("ERROR: Short Strangle requires --call-strike, --put-strike, --call-premium, --put-premium", file=sys.stderr)
            return None
        return build_short_strangle(
            args.call_strike, args.put_strike,
            args.call_premium, args.put_premium,
            lots, lot_size,
        )

    elif args.type == "iron-condor":
        required = [
            args.put_buy_strike, args.put_sell_strike,
            args.call_sell_strike, args.call_buy_strike,
            args.put_buy_premium, args.put_sell_premium,
            args.call_sell_premium, args.call_buy_premium,
        ]
        if not all(v is not None for v in required):
            print(
                "ERROR: Iron Condor requires --put-buy-strike, --put-sell-strike, "
                "--call-sell-strike, --call-buy-strike, --put-buy-premium, "
                "--put-sell-premium, --call-sell-premium, --call-buy-premium",
                file=sys.stderr,
            )
            return None
        return build_iron_condor(
            args.put_buy_strike, args.put_sell_strike,
            args.call_sell_strike, args.call_buy_strike,
            args.put_buy_premium, args.put_sell_premium,
            args.call_sell_premium, args.call_buy_premium,
            lots, lot_size,
        )

    elif args.type == "iron-butterfly":
        required = [
            args.put_buy_strike, args.atm_strike, args.call_buy_strike,
            args.put_buy_premium, args.atm_put_premium,
            args.atm_call_premium, args.call_buy_premium,
        ]
        if not all(v is not None for v in required):
            print(
                "ERROR: Iron Butterfly requires --put-buy-strike, --atm-strike, "
                "--call-buy-strike, --put-buy-premium, --atm-put-premium, "
                "--atm-call-premium, --call-buy-premium",
                file=sys.stderr,
            )
            return None
        return build_iron_butterfly(
            args.put_buy_strike, args.atm_strike, args.call_buy_strike,
            args.put_buy_premium, args.atm_put_premium,
            args.atm_call_premium, args.call_buy_premium,
            lots, lot_size,
        )

    print(f"ERROR: Unknown strategy type: {args.type}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
