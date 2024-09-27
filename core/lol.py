import requests
from django.core.cache import cache
from .utils import get_date, check_session_list, check_cache, cache_timeout
class LoLFixture():
    def __init__(self, club_name, tournament='Not Scheduled', round= 'Not Scheduled', opponent='Not Scheduled', timestamp='Not Scheduled'):
        self.club_name = club_name
        self.tournament = tournament
        self.round = round
        self.opponent = opponent
        self.date = get_date(timestamp) if isinstance(timestamp, int) else timestamp

# returns the next fixture of the given LoL club 
def get_LoL_fixtures(name, session_list):
    id_search_url = f"https://allsportsapi2.p.rapidapi.com/api/esport/search/{name}"
    session_list, headers = check_session_list(name, session_list, id_search_url)
    
    # query all IDs stored 
    all_fixtures = []
    # get cache data
    cached_data = cache.get('all_fixtures_lol')

    for names_ids in session_list:
        club_name = names_ids['name']
        club_id = names_ids['id']
 
        # if fixtures are in cache, get them
        in_cache = check_cache(cached_data, club_name, all_fixtures)

        if not in_cache:
            # get fixtures using the club id
            fixtures_url = f"https://allsportsapi2.p.rapidapi.com/api/esport/team/{club_id}/matches/next/0"
            fixture_response = requests.get(fixtures_url, headers=headers)
            print('api call for lol fixtures')

            # if Not Content response, create a default fixture
            if fixture_response.status_code == 204:
                fixture = LoLFixture(club_name)
            else:
                fixture_response_json = fixture_response.json()
                # tournament name
                tournament = fixture_response_json["events"][0]["tournament"]["uniqueTournament"]['name']

                round = fixture_response_json["events"][0]["tournament"]["name"]
                # opponent
                homeTeam = fixture_response_json["events"][0]["homeTeam"]["name"]
                awayTeam = fixture_response_json["events"][0]["awayTeam"]["name"]
                # opponent
                opponent = homeTeam if homeTeam != club_name else awayTeam

                # timestamp
                timestamp = fixture_response_json["events"][0]["startTimestamp"]

                fixture = LoLFixture(club_name, tournament, round, opponent, timestamp)

            all_fixtures.append(fixture)

    # save in cache until the end of the day
    cache.set('all_fixtures_lol', all_fixtures, timeout=cache_timeout().seconds)
    return all_fixtures, session_list