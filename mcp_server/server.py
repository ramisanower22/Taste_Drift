from mcp.server import MCPServer

from ml.taste_drift_pipeline import analyze_user


# ==========================================
# MCP SERVER
# ==========================================

mcp = MCPServer("Taste Drift")


# ==========================================
# TOOL 1: FULL ANALYSIS
# ==========================================

@mcp.tool()
def get_taste_drift(
    user_id: int,
    periods: int = 6
) -> dict:
    """
    Return the complete Taste Drift analysis for a user.
    """

    results = analyze_user(
        user_id=user_id,
        periods=periods
    )

    if results is None:
        return {
            "success": False,
            "message": "User could not be analyzed."
        }

    return {
        "success": True,
        "user_id": user_id,
        "periods": periods,
        "analysis": results
    }


# ==========================================
# TOOL 2: DRIFT TIMELINE
# ==========================================

@mcp.tool()
def get_drift_timeline(
    user_id: int,
    periods: int = 6
) -> dict:
    """
    Return only the taste drift timeline.
    """

    results = analyze_user(
        user_id=user_id,
        periods=periods
    )

    if results is None:
        return {
            "success": False,
            "message": "User could not be analyzed."
        }

    timeline = []

    for result in results:

        timeline.append({
            "from_period": result["from_period"],
            "to_period": result["to_period"],
            "similarity": result["similarity"],
            "drift": result["drift"]
        })

    return {
        "success": True,
        "user_id": user_id,
        "timeline": timeline
    }


# ==========================================
# TOOL 3: COMPARE TWO ADJACENT PERIODS
# ==========================================

@mcp.tool()
def compare_taste_periods(
    user_id: int,
    from_period: int,
    to_period: int,
    periods: int = 6
) -> dict:
    """
    Compare two adjacent taste periods.
    Example: period 3 to period 4.
    """

    results = analyze_user(
        user_id=user_id,
        periods=periods
    )

    if results is None:
        return {
            "success": False,
            "message": "User could not be analyzed."
        }

    for result in results:

        if (
            result["from_period"] == from_period
            and result["to_period"] == to_period
        ):

            return {
                "success": True,
                "user_id": user_id,
                "comparison": result
            }

    return {
        "success": False,
        "message": "Period comparison not found."
    }


# ==========================================
# TOOL 4: EXPLAIN DRIFT
# ==========================================

@mcp.tool()
def explain_drift(
    user_id: int,
    from_period: int,
    to_period: int,
    periods: int = 6
) -> dict:
    """
    Explain what changed between two taste periods
    using genres and tags.
    """

    results = analyze_user(
        user_id=user_id,
        periods=periods
    )

    if results is None:
        return {
            "success": False,
            "message": "User could not be analyzed."
        }

    for result in results:

        if (
            result["from_period"] == from_period
            and result["to_period"] == to_period
        ):

            return {
                "success": True,
                "user_id": user_id,
                "from_period": from_period,
                "to_period": to_period,
                "drift": result["drift"],
                "genre_changes": result["top_genre_changes"],
                "tag_changes": result["top_tag_changes"]
            }

    return {
        "success": False,
        "message": "Period comparison not found."
    }


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":
    mcp.run()