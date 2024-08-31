import requests
import datetime # datetime module
from datetime import timedelta, datetime as dt # datetime class
import os
from django.core.cache import cache

from dotenv import load_dotenv

load_dotenv('../.env')
# Get API key from environment variable
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

class FootballFixture():
    def __init__(self, club_name, venue, opponent, timestamp):
        self.club_name = club_name
        self.venue = venue
        self.opponent = opponent
        self.date = getDate(timestamp)

class TennisFixture():
    def __init__(self, player_name, tournament='Not Scheduled', round='Not Scheduled', opponent='Not Scheduled', timestamp='Not Scheduled'):
        self.player_name = player_name
        self.tournament = tournament
        self.round = round
        self.opponent = opponent
        self.date = getDate(timestamp) if isinstance(timestamp, int) else timestamp

# get date from the timestamp and format it
def getDate(timestamp):
    # if datetime object is passed
    if isinstance(timestamp, dt):
        fixture_date = timestamp
    else:
    # Get datetime object from int timestamp
        fixture_date = dt.fromtimestamp(timestamp)
    # Format the datetime object
    formatted_date = 'Today, ' + fixture_date.strftime('%H:%M') if fixture_date.date() == dt.today().date() else fixture_date.strftime('%a, %d %b, %H:%M')
    return formatted_date

    
# returns the next 4 fixtures of the given football club 
def getFootballFixtures(name, session_list):
    id_search_url = f"https://allsportsapi2.p.rapidapi.com/api/search/{name}"
    session_list, headers = check_session_list(name, session_list, id_search_url)
    
    # query all IDs stored 
    all_fixtures = []
    # get cache data
    cached_data = cache.get('all_fixtures_football')

    for names_ids in session_list:
        club_name = names_ids['name']
        club_id = names_ids['id']
 
        # if fixtures are in cache, get them
        in_cache = check_cache(cached_data, club_name, all_fixtures)

        if(not in_cache):
            # get fixtures using the club id
            fixtures_url = f"https://allsportsapi2.p.rapidapi.com/api/team/{club_id}/matches/next/0"
            fixtures_response = requests.get(fixtures_url, headers=headers).json()
            print('api call for football fix')
            # list of club fixtures
            fixtures = []
            # get the next 4 fixtures
            for i in range(4):
                # home or away
                venue = "Home" if fixtures_response["events"][i]["homeTeam"]["name"] == club_name else "Away"

                # opponent
                opponent = fixtures_response["events"][i]["awayTeam"]["name"] if venue == "Home" else fixtures_response["events"][i]["homeTeam"]["name"]

                # timestamp
                timestamp = fixtures_response["events"][i]["startTimestamp"]
                
                fixture = FootballFixture(club_name, venue, opponent, timestamp)
                fixtures.append(fixture)

            all_fixtures.append(fixtures)

    # save in cache until the end of the day
    cache.set('all_fixtures_football', all_fixtures, timeout=cache_timeout().seconds)
    return all_fixtures, session_list

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
        

# returns time left until the end of the day
# used to make the cache expire
def cache_timeout():
    dt = datetime.datetime.now()
    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min) - dt

# checks the session data
def check_session_list(name, session_list, id_search_url):
    session_list = [] if session_list is None else session_list

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
    }

    found_id = False
    # from the Get request
    if name == None:
        found_id = True
    else:
        # check if the given name is already on the session list
        if session_list:
            for session_names_ids in session_list:
                if name.casefold() in session_names_ids['name'].casefold():
                    found_id = True
                if sorted(name.casefold()) == sorted(session_names_ids['name'].casefold()):
                    found_id = True


    # if the name is not found, get the ID of the new name
    if not found_id:
        search_url = id_search_url
        search_response = requests.get(search_url, headers=headers).json()
        print('api call for ID')
        id = search_response["results"][0]["entity"]["id"]
        name = search_response["results"][0]["entity"]["name"]
        session_list.append({
            "name": name,
            "id": id
        })

    return session_list, headers

# get the requested fixtures if already in cache
def check_cache(cached_data, name, all_fixtures):

    if not cached_data:
        return False

    # check if we're dealing with tennis or football fixtures
    elif isinstance(cached_data[0], TennisFixture):
        for cached_fixture in cached_data:
            if cached_fixture.player_name == name:
                all_fixtures.append(cached_fixture)
                return True
        return False
    else:
        for cached_fixture_list in cached_data:
                for cached_fixture in cached_fixture_list:
                    if cached_fixture.club_name == name:
                        all_fixtures.append(cached_fixture_list)
                        return True
        return False

# returns the race name and datetime for the next F1 race                
def getF1RaceDetails():
    # jolpica-f1 API query
    race_details_json = requests.get('http://api.jolpi.ca/ergast/f1/current/next').json()
    race_name = race_details_json['MRData']['RaceTable']['Races'][0]['raceName']
    date = race_details_json['MRData']['RaceTable']['Races'][0]['date']
    time = race_details_json['MRData']['RaceTable']['Races'][0]['time']

    # datetime formatting
    datetime_str = f'{date} {time}'
    datetime_obj = dt.strptime(datetime_str, '%Y-%m-%d %H:%M:%SZ')
    datetime_obj_BST = datetime_obj + timedelta(hours=1)
    race_details = {
        "name": race_name,
        "datetime": getDate(datetime_obj_BST)
    }
    return race_details