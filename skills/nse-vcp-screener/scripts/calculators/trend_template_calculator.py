"""
Minervini's 7-Point Trend Template Calculator for Stage 2 identification.
Adapted for Indian markets (NSE/BSE).
"""

import pandas as pd


def calculate_trend_template(df: pd.DataFrame) -> dict:
    """
    Apply Minervini's 7-point Stage 2 trend template.

    Args:
        df: DataFrame with columns: Close (at minimum), indexed by date.
            Must have at least 200 rows of daily data.

    Returns:
        dict with keys:
            - criteria: list of 7 booleans (True = criterion met)
            - score: float 0-100
            - stage: int (1-4 estimated stage)
            - details: dict with MA values and comparisons
    """
    if len(df) < 200:
        return {
            "criteria": [False] * 7,
            "score": 0.0,
            "stage": 0,
            "details": {"error": "Insufficient data (need 200+ days)"},
        }

    close = df["Close"]
    current_price = float(close.iloc[-1])

    ma_50 = float(close.rolling(50).mean().iloc[-1])
    ma_150 = float(close.rolling(150).mean().iloc[-1])
    ma_200 = float(close.rolling(200).mean().iloc[-1])

    # Check if 200-day MA is trending up for at least 1 month (22 trading days)
    ma_200_series = close.rolling(200).mean()
    ma_200_month_ago = float(ma_200_series.iloc[-22]) if len(ma_200_series) >= 22 else ma_200
    ma_200_trending_up = ma_200 > ma_200_month_ago

    criteria = [
        current_price > ma_150,           # 1. Price > 150-day MA
        current_price > ma_200,           # 2. Price > 200-day MA
        ma_150 > ma_200,                  # 3. 150-day MA > 200-day MA
        ma_200_trending_up,               # 4. 200-day MA trending up ≥1 month
        ma_50 > ma_150,                   # 5. 50-day MA > 150-day MA
        ma_50 > ma_200,                   # 6. 50-day MA > 200-day MA
        current_price > ma_50,            # 7. Price > 50-day MA
    ]

    criteria_met = sum(criteria)
    score = criteria_met * (100 / 7)

    # Estimate stage
    if criteria_met >= 6:
        stage = 2
    elif current_price < ma_200 and ma_50 < ma_200:
        stage = 4
    elif current_price > ma_200 and ma_50 < ma_150:
        stage = 1
    else:
        stage = 3

    return {
        "criteria": criteria,
        "score": round(score, 1),
        "stage": stage,
        "details": {
            "price": current_price,
            "ma_50": round(ma_50, 2),
            "ma_150": round(ma_150, 2),
            "ma_200": round(ma_200, 2),
            "ma_200_trending_up": ma_200_trending_up,
            "criteria_met": criteria_met,
        },
    }
