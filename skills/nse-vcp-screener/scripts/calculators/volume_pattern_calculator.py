"""
Volume dry-up pattern calculator for VCP screening.
Measures whether volume is declining as the pattern tightens — a key VCP characteristic.
"""

import pandas as pd


def calculate_volume_pattern(df: pd.DataFrame) -> dict:
    """
    Calculate volume dry-up ratio and score.

    Args:
        df: DataFrame with 'Volume' column, at least 50 rows.

    Returns:
        dict with dry_up_ratio, score, and details.
    """
    if len(df) < 50 or "Volume" not in df.columns:
        return {
            "dry_up_ratio": 1.0,
            "score": 0.0,
            "details": {"error": "Insufficient data or no volume column"},
        }

    vol = df["Volume"]

    avg_50 = float(vol.tail(50).mean())
    avg_10 = float(vol.tail(10).mean())

    if avg_50 <= 0:
        return {
            "dry_up_ratio": 1.0,
            "score": 0.0,
            "details": {"error": "Zero or negative 50-day average volume"},
        }

    dry_up_ratio = avg_10 / avg_50

    score = _score_dry_up(dry_up_ratio)

    return {
        "dry_up_ratio": round(dry_up_ratio, 3),
        "score": round(score, 1),
        "details": {
            "avg_volume_50d": round(avg_50, 0),
            "avg_volume_10d": round(avg_10, 0),
        },
    }


def _score_dry_up(ratio: float) -> float:
    """Score volume dry-up ratio on 0-100 scale."""
    if ratio < 0.40:
        return 90
    elif ratio < 0.50:
        return 80
    elif ratio < 0.60:
        return 70
    elif ratio < 0.70:
        return 60
    elif ratio < 0.80:
        return 45
    elif ratio < 0.90:
        return 30
    else:
        return 15
