from tinydb import TinyDB, Query
import json, re, sys, argparse, os
from datetime import datetime

# db = TinyDB('accuw_db.json')
# Location = db.table('Location')
# Profile = db.table('Profile')

# if "ACW_API_KEY" in os.environ:
#     API_KEY = os.environ['ACW_API_KEY']
#     Profile.upsert({'api_key':API_KEY}, Query().api_key.exists())
# else:
#     API_KEY = Profile.search(Query().api_key)
#     if API_KEY == []:
#         sys.exit("No API key found")
#         API_KEY = API_KEY[0]['api_key']

# def is_input_inputted(input_bar, table, field_name):
#     if input_bar is None:
#         input_bar = table.search(Query()[field_name])
#         if input_bar == []:
#             parser.print_help()
#             sys.exit()
#         input_bar = input_bar[0][field_name]
#     else:
#         table.upsert({field_name:input_bar}, Query()[field_name].exists())
#     return input_bar
# parser = argparse.ArgumentParser(description='Accuweather Forecast for Python')
# parser.add_argument('-l', action="store", dest="location", help='Location for weather forecast, e.g. "London"')
# parser.add_argument('-m', action="store", dest="metric", choices=['c', 'f'], help='metric for weather forecast, c or f', default="c", type=str.lower)
# args = parser.parse_args()

# location = is_input_inputted(args.location, Profile, "last_location")
# metric = is_input_inputted(args.metric, Profile, "last_metric")


# if (Location.count(Query()) == 0):
#     url = f"http://dataservice.accuweather.com/locations/v1/topcities/150?api_key={API_KEY}"
#     json_data = getJSONfromUrl(url)

#     for p in json_data:
#         Location.insert({'name': p['LocalizedName'], 'key': p['Key'], 'english_name': p['EnglishName'],
#         'administrative_area': p['AdministrativeArea']['ID'], 'country': p['Country']['EnglishName']})
#         print(p)
# location_from_db = Location.search(Query().name.matches(location, flags=re.IGNORECASE))

# if location_from_db == []:
#     url = f"http://dataservice.accuweather.com/locations/v1/topcities/150?api_key={API_KEY}&amp;q={location}"
#     json_data = getJSONfromUrl(url)
# if json_data == []:
#     sys.exit(f"No location found for '{location}' from Accuweather API")
# else:
#     for p in json_data:
#         Location.insert({'name': location, 'key': p['Key'], 'english_name': p['EnglishName'],
#         'administrative_area': p['AdministrativeArea']['ID'], 'country': p['Country']['EnglishName']})
#         break
#     location_from_db = Location.search(Location.name.matches(location, flags=re.IGNORECASE))

# location_key = location_from_db[0]['key']
# admin_area = location_from_db[0]['administrative_area']
# country = location_from_db[0]['country']