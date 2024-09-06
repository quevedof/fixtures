# Fixtures Web App
A web app that provides fixtures of different sports and e-sports.

Technologies used: Django's session, cache, and Model-View-Template (MVT) architecture; WhiteNoise package that allows the app to serve its own static files making it ready for production; https://supabase.com/ for PostgreSQL database deployment; https://vercel.com/ as a PaaS for hosting the web app.

APIs used: https://rapidapi.com/fluis.lacasse/api/allsportsapi2 (football & tennis); https://api.jolpi.ca/ergast/f1/ (formula 1)

Hosted here: https://fixturesation.vercel.app/

### Features
- Football/LoL/Valorant: takes a club name and returns the date, time, opponent, and venue (football) of the next four fixtures.
- Tennis: takes a player name and returns the date, time, opponent, tournament, and round of the their next fixture.
- Formula 1: displays the date, time, and starting grid (if available) of the next race; the last race results, and the current championship driver standings.

### Prerequisites
- Python 3.x

### Installation
1. Clone the repository
    ```
    git clone https://github.com/quevedof/fixtures.git

    cd fixtures
    ```

2. Enable virtual environment (optional)
    ```
    python -m venv .venv
    .venv/Scripts/activate
    ```
3. Install dependecies
    ```
    pip install -r requirements.txt
    ```
4. API used is AllSportsAPI from Rapid API, can be found here: https://rapidapi.com/fluis.lacasse/api/allsportsapi2 \
    Copy the env file and add your api key
    ```
    cp -- .env.copythis .env
    ```
5. Changes in the project's settings.py file to use Django's built-in DB for local development.
    ```python
    SECRET_KEY = <Django secret key>
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```
    To generate a Django secret key, open a Python shell in your project directory and run the following commands:
    ```
    python3 manage.py shell

    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ```
6. Run the server using django shortcuts
    ```
    # Make migrations
    django mm
    django m

    # Run the server
    djang r
    ```
