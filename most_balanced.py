from utilities import american_to_decimal, find_most_balanced


def find_most_balanced_totals(outcomes: list[dict]) -> tuple[dict, dict]:
    """ Find the most balanced over/under totals lines (lowest price difference or straddle) from a list of alternate totals outcomes
    
    Prices must be in decimal format. utilities.py contains functions to convert between American and decimal odds formats
    """
    overs = list(filter(lambda x: x['name'] == 'Over', outcomes))
    unders = list(filter(lambda x: x['name'] == 'Under', outcomes))
    return find_most_balanced(overs, unders)

def find_most_balanced_team_totals(outcomes: list[dict], home_team: str, away_team: str) -> tuple[tuple[dict, dict], tuple[dict, dict]]:
    """ Find the most balanced over/under team totals lines (lowest price difference or straddle) from a list of alternate team totals outcomes
    
    Prices must be in decimal format. utilities.py contains functions to convert between American and decimal odds formats
    """
    home_team_overs = list(filter(lambda x: x['name'] == 'Over' and x['description'] == home_team, outcomes))
    home_team_unders = list(filter(lambda x: x['name'] == 'Under' and x['description'] == home_team, outcomes))
    home_team_most_balanced = find_most_balanced(home_team_overs, home_team_unders)

    away_team_overs = list(filter(lambda x: x['name'] == 'Over' and x['description'] == away_team, outcomes))
    away_team_unders = list(filter(lambda x: x['name'] == 'Under' and x['description'] == away_team, outcomes))
    away_team_most_balanced = find_most_balanced(away_team_overs, away_team_unders)    

    return (home_team_most_balanced, away_team_most_balanced)

if __name__ == '__main__':
    # Add response from the event-odds endpoint here. It should be a dictionary.
    # Odds must be in decimal format. If necessary, they can be converted using the american_to_decimal function from utilities.py
    response = ...
    
    # This example uses the first bookmaker
    bookmaker = response['bookmakers'][0]

    # Find the most balanced totals lines
    alternate_totals = list(filter(lambda x: x['key'] == 'alternate_totals', bookmaker['markets']))[0]
    if not alternate_totals:
        print("Alternate totals market not found from first bookmaker")
        print()
    
    else:
        most_balanced_totals = find_most_balanced_totals(alternate_totals['outcomes'])
        print()
        print("Most balanced totals")
        print(most_balanced_totals)
        print()


    # Find the most balanced home/away lines for alternate team totals
    alternate_team_totals = list(filter(lambda x: x['key'] == 'alternate_team_totals', bookmaker['markets']))[0]
    if not alternate_team_totals:
        print("Alternate team totals market not found from first bookmaker")
    
    else:
        home_team_most_balanced, away_team_most_balanced = find_most_balanced_team_totals(alternate_team_totals['outcomes'], response['home_team'], response['away_team'])

        print(f"Most balanced team totals for {response['home_team']}")
        print(home_team_most_balanced)
        print()
        print(f"Most balanced team totals for {response['away_team']}")
        print(away_team_most_balanced)
        print()
