import requests
from datetime import timedelta, datetime as dt # datetime class
from .utils import getDate

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

# returns the current championship standings
def getF1DriverStandings():
    # get the current season
    current_season_json = requests.get('http://api.jolpi.ca/ergast/f1/current/').json()
    current_season = current_season_json['MRData']['RaceTable']['season']

    # get standings
    driver_standings_json = requests.get(f'https://api.jolpi.ca/ergast/f1/{current_season}/driverstandings/').json()
    driver_standings=[]

    for driver in driver_standings_json['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
        pos = driver['position']
        given_name = driver['Driver']['givenName']
        family_name = driver['Driver']['familyName']
        nationality = driver['Driver']['nationality']
        car= driver['Constructors'][0]['name']
        points = driver['points']
        driver = {
            "pos": pos,
            "driver": f"{given_name} {family_name}",
            "nationality": nationality,
            "car": car,
            "points": points,
        }
        driver_standings.append(driver)

    return driver_standings

# returns results of the last F1 race
def getF1LastRaceResults(): 
    # get results
    last_race_results_json = requests.get('http://api.jolpi.ca/ergast/f1/current/last/results/').json()
    race_name = last_race_results_json['MRData']['RaceTable']['Races'][0]['raceName']

    last_race_results=[]
    for driver in last_race_results_json['MRData']['RaceTable']['Races'][0]['Results']:
        pos = driver['position']
        given_name = driver['Driver']['givenName']
        family_name = driver['Driver']['familyName']
        car= driver['Constructor']['name']
        # drivers with +1 laps have no time
        try:
            time = driver['Time']['time']
        except KeyError:
            time = driver['status']
        points = driver['points']
        driver = {
            "race_name": race_name,
            "pos": pos,
            "driver": f"{given_name} {family_name}",
            "car": car,
            "time": time,
            "points": points,
        }
        last_race_results.append(driver)

    return last_race_results