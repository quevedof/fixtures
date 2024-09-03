import requests
from django.core.cache import cache
from datetime import datetime as dt
import os
from dotenv import load_dotenv
from .utils import getDate, check_session_list, check_cache, cache_timeout


load_dotenv('../.env')
# Get API key from environment variable
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

class TennisFixture():
    def __init__(self, player_name, tournament='Not Scheduled', round='Not Scheduled', opponent='Not Scheduled', timestamp='Not Scheduled'):
        self.player_name = player_name
        self.tournament = tournament
        self.round = round
        self.opponent = opponent
        self.date = getDate(timestamp) if isinstance(timestamp, int) else timestamp

# returns the next tournament for the given player
def getTennisFixtures(name, session_list):
    id_search_url = f"https://allsportsapi2.p.rapidapi.com/api/tennis/search/{name}"
    session_list, headers = check_session_list(name, session_list, id_search_url)

    # query all IDs stored 
    all_fixtures = []
    # get cache data
    cached_data = cache.get('all_fixtures_tennis')

    for names_ids in session_list:
        player_name = names_ids['name']
        player_id = names_ids['id']

        # if fixtures are in cache, get them
        in_cache = check_cache(cached_data, player_name, all_fixtures)


        if(not in_cache):
            # get fixtures using the player id
            fixture_url = f"https://allsportsapi2.p.rapidapi.com/api/tennis/player/{player_id}/events/next/0"
            fixture_response = requests.get(fixture_url, headers=headers)
            print('api call for tennis fixtures')
            # if Not Content response, create a default fixture
            if fixture_response.status_code == 204:
                fixture = TennisFixture(player_name)
            else:
                fixture_response_json = fixture_response.json()
                # tournament name
                tournament = fixture_response_json["events"][0]["tournament"]["name"]
                # round info
                round = fixture_response_json["events"][0]["roundInfo"]["name"]

                # opponent
                homeTeam = fixture_response_json["events"][0]["homeTeam"]["name"]
                awayTeam = fixture_response_json["events"][0]["awayTeam"]["name"]
                opponent = homeTeam if homeTeam != player_name else awayTeam

                # timestamp
                timestamp = fixture_response_json["events"][0]["startTimestamp"]

                fixture = TennisFixture(player_name, tournament, round, opponent, timestamp)

            all_fixtures.append(fixture)
        
    cache.set('all_fixtures_tennis', all_fixtures, timeout=cache_timeout().seconds)       
    return all_fixtures, session_list

# gets the top 100 players in the ATP ranking
def getATPList():
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
    }
    # check if cached
    cached_atp_list = cache.get('atp_list')
    if cached_atp_list:
        # refresh the cache if current day is Monday
        # ATP rankings are updated every Monday
        if dt.today().date().weekday() == 0:
            atp_list_response = requests.get('https://allsportsapi2.p.rapidapi.com/api/tennis/rankings/atp', headers=headers).json()
            atp_list =[]
            for i in range(100):
                atp_list.append(atp_list_response['rankings'][i]['team']['name'])
            
            atp_list.append('Nadal R.') # personal favorite, not in top 100
            cache.set('atp_list', atp_list)
            return atp_list
        else:
            return cached_atp_list
    
    else:
        atp_list_response = requests.get('https://allsportsapi2.p.rapidapi.com/api/tennis/rankings/atp', headers=headers).json()
        atp_list =[]
        for i in range(100):
            atp_list.append(atp_list_response['rankings'][i]['team']['name'])
        
        atp_list.append('Nadal R.') # personal favorite, not in top 100
        cache.set('atp_list', atp_list)
        return atp_list