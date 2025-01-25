import argparse

import requests


# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = args.api_key or 'YOUR_API_KEY'

# Sport key
# Find sport keys from the /sports endpoint below, or from https://the-odds-api.com/sports-odds-data/sports-apis.html
# Ensure the sport key is in-season before running this script
SPORT = 'basketball_nba'

# Bookmaker regions
# uk | us | us2 | eu | au. Multiple can be specified if comma delimited.
# More info at https://the-odds-api.com/sports-odds-data/bookmaker-apis.html
REGIONS = 'us'

# Odds markets
# More info at https://the-odds-api.com/sports-odds-data/betting-markets.html
# Note only featured markets (h2h, spreads, totals) are available with the odds endpoint.
MARKETS = 'h2h_q1,player_points,player_rebounds'

# Odds format
# decimal | american
ODDS_FORMAT = 'american'

# Date format
# iso | unix
DATE_FORMAT = 'iso'


# First get a list of events
events_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/events', params={
    'api_key': API_KEY,
})


if events_response.status_code != 200:
    print(f'Failed to get sports: status_code {events_response.status_code}, response body {events_response.text}')
    exit()

events_json = events_response.json()
if len(events_json) == 0:
    print('No events found')
    exit()


print(f'Found {len(events_json)} events. Querying the first event')
first_event = events_json[0]
first_event_id = first_event['id']

odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/events/{first_event_id}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
})

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    # pretty print odds response
    print(json.dumps(odds_json, indent=2))
    
    # Check the usage quota
    print('Total credits remaining', odds_response.headers['x-requests-remaining'])
    print('Total credits used', odds_response.headers['x-requests-used'])
