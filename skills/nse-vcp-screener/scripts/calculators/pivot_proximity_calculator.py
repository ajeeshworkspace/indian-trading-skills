"""
Pivot proximity calculator.
Scores how close the current price is to the VCP breakout pivot level.
"""


def calculate_pivot_proximity(current_price: float, pivot: float) -> dict:
    """
    Calculate distance from pivot and score.

    Args:
        current_price: Current stock price
        pivot: Breakout pivot level

    Returns:
        dict with distance_pct, score, and position
    """
    if pivot <= 0 or current_price <= 0:
        return {
            "distance_pct": 0.0,
            "score": 0.0,
            "position": "invalid",
        }

    distance_pct = (pivot - current_price) / pivot * 100

    if distance_pct < 0:
        # Already above pivot (broken out)
        score = 50.0
        position = "above_pivot"
    elif distance_pct <= 3:
        score = 90.0
        position = "near_pivot"
    elif distance_pct <= 5:
        score = 75.0
        position = "approaching_pivot"
    elif distance_pct <= 8:
        score = 60.0
        position = "moderate_distance"
    elif distance_pct <= 12:
        score = 45.0
        position = "far_from_pivot"
    elif distance_pct <= 20:
        score = 30.0
        position = "very_far"
    else:
        score = 15.0
        position = "too_far"

    return {
        "distance_pct": round(abs(distance_pct), 2),
        "score": score,
        "position": position,
    }
