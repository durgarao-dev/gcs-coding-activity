import requests
import click
import json
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('OPEN_WEATHER_API_KEY')
api_url = "https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_id}&units=imperial"
fav_file = 'favorites.json'

# Load existing favorites from a file or create a new list
if os.path.exists(fav_file):
  with open(fav_file, 'r') as file:
    FAV_LIST = json.load(file)
else:
  FAV_LIST = []

# Function to add favorites to list
def save_favorites():
    with open(fav_file, 'w') as file:
        json.dump(FAV_LIST , file)


def get_city_weather(city_name):
    try: 
        api_resp = requests.get(api_url.format(location=city_name, api_id=api_key))
        api_resp.raise_for_status()
        return api_resp.json()
    except requests.exceptions.RequestException as err:
        click.echo("Error fetching weather data: {}".format(err))
        return None

def parse_weather_data(api_resp):
    name= api_resp['name']
    temperature= api_resp['main']['temp']
    humidity= api_resp['main']['humidity']
    wind_speed= api_resp['wind']['speed']
    weather_details = (
       "Weather Details for {}\n"
       "Temperature: {}°F\n"
       "Humidity: {}%\n" 
       "Wind Speed: {} miles/hr\n").format(name,temperature, humidity, wind_speed)
    return weather_details

@click.group()
def weather():
  """A CLI application for getting weather details of a city\n
    You can add upto 3 cities to your fav list\n
    Use the below commands to get started \n
    use " " or '' for city names with more than one word\n
    Example: python weather.py search "new york" """
  pass

# Command to search for weather details
@weather.command(help="Search for weather details of a city")
@click.argument('city_name')
def search(city_name):
  api_resp = get_city_weather(city_name)
  if api_resp is None:
    click.echo("Failed to fetch city weather data for the city.")
    return
  click.echo(parse_weather_data(api_resp))


# add command to add cities to favorites list
@weather.command(help="Add a city to favorites list")
@click.argument('city_name')
def add(city_name):
    if len(FAV_LIST) >= 3:
        click.echo("Max allowed cities limit exceeded!!")
    elif city_name in FAV_LIST:
        click.echo("Error: {} already exists in favorites list.".format(city_name))
    elif len(FAV_LIST) < 3:
        api_resp = get_city_weather(city_name)
        if api_resp is None or len(city_name) == 0:
            click.echo("Failed to fetch city weather data for the city.")
            return
        else:
            FAV_LIST.append(city_name)
            save_favorites()
            click.echo("Added {} to favorites list.".format(city_name))

# get command to get the list of favorites cities
@weather.command(help="Get the list of favorite cities")
def get():
  if len(FAV_LIST) == 0:
    click.echo("No cities in favorites list.")
  else:
    click.echo("Favourite cities are: " + ", ".join(FAV_LIST))

# Replaces existing fav city with the new city provided by user
@weather.command(help="Update a city in favorites list with a new city")
@click.argument('old_city')
@click.argument('new_city')
def update(old_city, new_city):
  if old_city in FAV_LIST:
        if new_city in FAV_LIST:
            click.echo("Error: {} already exists in favorites list.".format(new_city))
        else:
            FAV_LIST[FAV_LIST.index(old_city)] = new_city
            save_favorites()
            click.echo("Replaced {} with {} in favorites list.".format(old_city, new_city))
  else:
    click.echo("Old city not found in favorite list.")

if __name__ == "__main__":
  weather()
