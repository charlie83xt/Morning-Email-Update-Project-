from cmath import e
from curses import raw
from sqlite3 import Timestamp
# import urllib.request
import json
import random
import tweepy as tw
from datetime import datetime
import requests
import os

# Accuweather credentials
LOCATION_KEY = "328328"
API_KEY = os.environ.get("ACC_API_KEY")

# Twitter Credentials
T_API_KEY = os.environ.get('T_API_KEY') #TWITTER_API_KEY
API_SECRET_KEY = os.environ.get('API_SECRET_KEY') #TWITTER_SECRET_KEY
BEARER_TOKEN = os.environ.get('BEARER_TOKEN') # TWITTER_BEARER
auth = tw.OAuthHandler(T_API_KEY, API_SECRET_KEY)
# api = tw.API(auth, wait_on_rate_limit=True)
WOEID = 23424975 # Default location United kingdom



def get_random_quote(quotes_file = "quotes.txt"):

    try: #read quote from txt file 
        with open(quotes_file) as text:
            phrase = text.readlines()
    except Exception as e: # Here we return default quote to help the program to go forward
        phrase = ["And suddenly, one day I learned that only myself would take me out from the dark hole"+"- Torres"]

    return random.choice(phrase)

def getFormattedDateTime(datestr):

    p_datestr_format = ''.join(datestr.rsplit(":", 1))
    date_object = datetime.strptime(p_datestr_format, '%Y-%m-%dT%H:%M:%S%z')
    return date_object.strftime("%H:%M %A, %d %B %Y Timezone:%z")

def getJSONfromUrl(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data

def get_weather_forecast(location_key=LOCATION_KEY):

    try:
        # Retrieve accuweather data passing API and LOCATION in url"
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={API_KEY}&details=true&metric=true"
        json_data = getJSONfromUrl(url)

        # Retrieve location passing LOCATION in url"
        location_url =  f"http://dataservice.accuweather.com/locations/v1/{location_key}?apikey={API_KEY}&details=true"
        location_data = getJSONfromUrl(location_url)

        forecast = {
            "location" : location_data["LocalizedName"],
            "admin_area": location_data["AdministrativeArea"]["EnglishType"],
            "country": location_data["Country"]["EnglishName"],
            "Summary": json_data['Headline']['Text'],
            "Date": getFormattedDateTime( json_data['DailyForecasts'][0]['Date'] ),
            "Min Temperature": json_data['DailyForecasts'][0]['Temperature']['Minimum']['Value'],
            "Min_Temp_unit": json_data['DailyForecasts'][0]['Temperature']['Minimum']['Unit'],
            "Max Temperature": json_data['DailyForecasts'][0]['Temperature']['Maximum']['Value'],
            "Max_Temp_unit": json_data['DailyForecasts'][0]['Temperature']['Maximum']['Unit'],
            "Description": json_data['DailyForecasts'][0]['Day']['LongPhrase'],
            "Rain Probability": json_data['DailyForecasts'][0]['Day']['RainProbability'],
            "Snow Probability": json_data['DailyForecasts'][0]['Day']['SnowProbability'],
            "Wind Speed": json_data['DailyForecasts'][0]['Day']['WindGust']['Speed']['Value'],
            "Wind_Sp_unit": json_data['DailyForecasts'][0]['Day']['WindGust']['Speed']['Unit'],
            "Visit": json_data['Headline']['MobileLink'] 
        }
        # print(f"Location: {location}, {admin_area}, {country}")
        return forecast

    except Exception as e:
        print(e)

def get_twitter_trends(place = WOEID):
    try:
        # Calling the API
        api = tw.API(auth)

        # Fetching the trends
        trending_topic = api.get_place_trends(place)

        # Store trends in list
        # trends = {"Trends": list()}
        # for value in trending_topic:
        #     for trend in value['trends']:
        #         trends['Trends'].append({trend['name']: trend['url']})

        # return f"The top trends for the selected location are:\n {trending_topic}"
        return trending_topic

    except Exception as e:
        print(e)

def get_wikipedia_article():
    pass

if __name__=='__main__':
    ### test get_random_quote() ###
    # print('\nTesting quote generation...')

    # quote = get_random_quote()
    # print(f' -Random Quote is {quote}')

    # quote = get_random_quote(quotes_file = None)
    # print(f' - Default quote is {quote}')
    

    ### test get_weather_forecast() ###
    '''
    forecast = get_weather_forecast() #Forecast for default location "London"
    if forecast:
        print(f'\nWeather forecast for {forecast["location"]}, {forecast["country"]} is ...' )
        print(f' - {forecast["Date"]} | {forecast["Min Temperature"]}ºC | {forecast["Description"]}')
        print(f' - {forecast["Wind Speed"]} | {forecast["Max Temperature"]}ºC')

    barcelona = "307297" # Barcelona's accuweather location code
    forecast = get_weather_forecast(location_key = barcelona) # Forecast for Barcelona Spain
    if forecast:
        print(f'\nWeather forecast for {forecast["location"]}, {forecast["country"]} is ...' )
        print(f' - {forecast["Date"]} | {forecast["Min Temperature"]}ºC | {forecast["Description"]}')
        print(f' - {forecast["Wind Speed"]} | {forecast["Max Temperature"]}ºC')
    
    forecast = get_weather_forecast(location_key = "26301") # Invalid location code
    if forecast:
        print(f'\nWeather forecast for {forecast["location"]}, {forecast["country"]} is ...' )
        print(f' - {forecast["Date"]} | {forecast["Min Temperature"]}ºC | {forecast["Description"]}')
        print(f' - {forecast["Wind Speed"]} | {forecast["Max Temperature"]}ºC')
        if forecast is None:
            print("Weather forecast for invalid coordinates returned None")
    '''

    ### test get Twitter trends ###
    trends = get_twitter_trends()
    if trends:
        print('Top 10 Twitter trends in London are... ')
        for trend in trends[0:10]:
            print(f' - {trend["trends"][0]["name"]} : {trend["trends"][0]["url"]}')
            # print(f' - {trend["name"]}:{trend["url"]}')
            # print(trend["trends"][0])
    
    trends = get_twitter_trends(place = 23424977)
    if trends:
        print('Top 10 Twitter trends in United States are... ')
        for trend in trends[0:10]:
            print(f' - {trend["trends"][0]["name"]} : {trend["trends"][0]["url"]}')
            # print(trend["trends"][0])
            # print(f' - {trend["name"]}:{trend["url"]}')

    trends = get_twitter_trends(place = 1)
    if trends == None:
        print('\nTwitter trends for invalid location returned None')
        
