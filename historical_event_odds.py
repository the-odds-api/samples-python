""" Sample code to query historical odds for any market for a single event

Historical odds are only available on paid usage plans.

More information can be found at https://the-odds-api.com/historical-odds-data/
"""

import argparse
import json

import requests


# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Historical odds sample code')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = args.api_key or 'YOUR_API_KEY'

# Sport key
# More info at https://the-odds-api.com/sports-odds-data/sports-apis.html
SPORT = 'basketball_nba'

# Bookmaker regions
# uk | us | eu | au. Multiple can be specified if comma delimited.
# More info at https://the-odds-api.com/sports-odds-data/bookmaker-apis.html
REGIONS = 'us' 

# Odds markets
# Multiple can be specified if comma delimited
# More info at https://the-odds-api.com/sports-odds-data/betting-markets.html
MARKETS = 'h2h_h1,player_points,player_rebounds,player_assists' 

# Odds format
# decimal | american
ODDS_FORMAT = 'american'

# Date format
# iso | unix
DATE_FORMAT = 'iso'

# Historical timestamp
# Must be in ISO8601 format
DATE = '2023-11-01T20:00:00Z'

# Event ID
# A list of event ids at this timestamp can be found using the events endpoint, for example:
# https://api.the-odds-api.com/v4/historical/sports/{sport_key}/events?apiKey={API_KEY}&date={DATE}
# This event id is for the Trail Blazers @ Pistons game on 2023-11-01
EVENT_ID = '80ef276018c492f53d3c94229942e855'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Query bookmaker odds for live and upcoming games as they were at the specified DATE parameter.
# The usage quota cost = 10 x [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs-3
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get(f'https://api.the-odds-api.com/v4/historical/sports/{SPORT}/events/{EVENT_ID}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
    'date': DATE,
})

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()

    print(json.dumps(odds_json['data'], indent=4))

    print(f"Timestamp: {odds_json['timestamp']}")
    print(f"Previous available timestamp: {odds_json['previous_timestamp']}")
    print(f"Next available timestamp: {odds_json['next_timestamp']}")
    
    # Check the usage quota
    print('Remaining credits', odds_response.headers['x-requests-remaining'])
    print('Used credits', odds_response.headers['x-requests-used'])
