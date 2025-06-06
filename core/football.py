import requests
from django.core.cache import cache
from .utils import get_date, check_session_list, check_cache, cache_timeout
class FootballFixture():
    def __init__(self, club_name, venue, opponent, timestamp, tournament):
        self.club_name = club_name
        self.venue = venue
        self.opponent = opponent
        self.date = get_date(timestamp)
        self.tournament = tournament

# returns the next 4 fixtures of the given football club 
def get_football_fixtures(name, session_list):
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

        if not in_cache:
            # get fixtures using the club id
            fixtures_url = f"https://allsportsapi2.p.rapidapi.com/api/team/{club_id}/matches/next/0"
            fixtures_response = requests.get(fixtures_url, headers=headers).json()
            print('api call for football fixture')
            # list of fixtures
            fixtures = []

            # number of fixtures
            fixtures_num = 4 if len(fixtures_response["events"]) > 3 else len(fixtures_response["events"])
            # get the next fixtures
            for i in range(fixtures_num):
                # home or away
                venue = "Home" if fixtures_response["events"][i]["homeTeam"]["name"] == club_name else "Away"

                # opponent
                opponent = fixtures_response["events"][i]["awayTeam"]["name"] if venue == "Home" else fixtures_response["events"][i]["homeTeam"]["name"]

                # timestamp
                timestamp = fixtures_response["events"][i]["startTimestamp"]

                # tournament
                tournament = fixtures_response["events"][i]["tournament"]["name"]
                
                fixture = FootballFixture(club_name, venue, opponent, timestamp, tournament)
                fixtures.append(fixture)

            all_fixtures.append(fixtures)

    # save in cache until the end of the day
    cache.set('all_fixtures_football', all_fixtures, timeout=cache_timeout().seconds)
    return all_fixtures, session_list