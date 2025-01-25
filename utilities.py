""" This file contains miscellaneous functions that can be useful when working with data from The Odds API
"""

def american_to_decimal(am_odd: float) -> float:
    """ Convert American odds to decimal odds
    """
    if am_odd < 0:
        odd = 1 - 100 * 1.0 / am_odd
    else:
        odd = 1 + am_odd * 1.0 / 100
    
    return odd

def decimal_to_american(odd: float) -> int:
    if odd == 1:
        # Decimal odds of 1 have no payout and are not bettable
        return 0

    if odd < 2:
        return int(round(100 / (1 - odd), 0))
    else:
        return int(round(100 * (odd - 1), 0))

def find_most_balanced(side_1_outcomes: list[dict], side_2_outcomes: list[dict], american_odds_format: bool) -> tuple[dict, dict]:
    """ When working with alternate markets, this function can be used to find the most balanced lines (the lines with the lowest price difference or straddle).
    """
    side_1_by_point = {x['point']: x for x in side_1_outcomes}
    side_2_by_point = {x['point']: x for x in side_2_outcomes}

    diffs = {}
    for point in side_1_by_point:
        if point not in side_2_by_point:
            continue
        
        side_1 = side_1_by_point[point]
        side_2 = side_2_by_point[point]
        
        if american_odds_format:
            diffs[point] = abs(american_to_decimal(side_1['price']) - american_to_decimal(side_2['price']))
        else:
            diffs[point] = abs(side_1['price'] - side_2['price'])

    # Find the point with the smallest price difference
    most_balanced_point = min(diffs, key=diffs.get)
    return (side_1_by_point[most_balanced_point], side_2_by_point[most_balanced_point])
