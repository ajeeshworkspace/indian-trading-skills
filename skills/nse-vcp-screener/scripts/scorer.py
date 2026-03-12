"""
VCP Composite Scorer.
Combines 5 component scores into a single 0-100 composite score.
"""


WEIGHTS = {
    "trend_template": 0.25,
    "contraction_quality": 0.25,
    "volume_pattern": 0.20,
    "pivot_proximity": 0.15,
    "relative_strength": 0.15,
}


def calculate_composite_score(
    trend_score: float,
    contraction_score: float,
    volume_score: float,
    pivot_score: float,
    rs_score: float,
) -> dict:
    """
    Calculate the weighted composite score.

    Args:
        trend_score: Trend template score (0-100)
        contraction_score: Contraction quality score (0-100)
        volume_score: Volume dry-up score (0-100)
        pivot_score: Pivot proximity score (0-100)
        rs_score: Relative strength score (0-100)

    Returns:
        dict with composite_score, components, and quality rating.
    """
    composite = (
        trend_score * WEIGHTS["trend_template"]
        + contraction_score * WEIGHTS["contraction_quality"]
        + volume_score * WEIGHTS["volume_pattern"]
        + pivot_score * WEIGHTS["pivot_proximity"]
        + rs_score * WEIGHTS["relative_strength"]
    )

    composite = round(composite, 1)

    if composite >= 80:
        quality = "Excellent"
    elif composite >= 65:
        quality = "Good"
    elif composite >= 50:
        quality = "Fair"
    else:
        quality = "Poor"

    return {
        "composite_score": composite,
        "quality": quality,
        "components": {
            "trend_template": {"score": trend_score, "weight": WEIGHTS["trend_template"]},
            "contraction_quality": {"score": contraction_score, "weight": WEIGHTS["contraction_quality"]},
            "volume_pattern": {"score": volume_score, "weight": WEIGHTS["volume_pattern"]},
            "pivot_proximity": {"score": pivot_score, "weight": WEIGHTS["pivot_proximity"]},
            "relative_strength": {"score": rs_score, "weight": WEIGHTS["relative_strength"]},
        },
    }
