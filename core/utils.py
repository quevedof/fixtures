import requests
import datetime # datetime module
from datetime import datetime as dt # datetime class
import os
from dotenv import load_dotenv
from django.utils import timezone
import zoneinfo

load_dotenv('../.env')
# Get API key from environment variable
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

# get date from the timestamp and format it
def getDate(timestamp):
    # if datetime object is passed, it's ready to be formatted
    if isinstance(timestamp, dt):
        fixture_date = timestamp
    else:
        # Get datetime object from int timestamp
        timezone.activate(zoneinfo.ZoneInfo('Europe/London'))
        print(timezone.get_current_timezone())

        fixture_date = dt.fromtimestamp(timestamp)
        tzed_fixture_date = timezone.localtime(timezone.make_aware(fixture_date))
        print(tzed_fixture_date)

    # Format the datetime object
    formatted_date = 'Today, ' + fixture_date.strftime('%H:%M') if fixture_date.date() == dt.today().date() else fixture_date.strftime('%a, %d %b, %H:%M')
    return formatted_date
        
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
    #from .tennis import TennisFixture

    if not cached_data:
        return False

    # check if we're dealing with tennis or football fixtures
    elif not isinstance(cached_data[0], list):
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
