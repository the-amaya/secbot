import discord
from discord.ext import commands
import json
import requests
import io
from PIL import Image
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import configparser
import datetime

# TODO better embed formatting. maybe build a graph or something for the forecast
# TODO add regional radar composites as well as the conus

# TODO we should also accept a callsign and just return that radar loop.
#  probably implement when we implement the regions


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.radar_stations = json.load(open("radar_stations.json"))
        self.settings_file_name = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file_name)
        self.geolocator = Nominatim(user_agent=self.config['weather']['useragent'])

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog weather is ready.')

    @commands.command()
    async def radar(self, ctx, *, location):
        """
        Get a radar image from the NWS based on the users provided zip code or city.
        """
        try:
            location = self.geolocator.geocode(location, exactly_one=True, country_codes='us')
            primary_radar_station, secondary_radar_station = self.get_radar_station(location.latitude, location.longitude)
            if self.get_radar_health(primary_radar_station["properties"]["icao"]) == 'ok':
                radar_station_call = primary_radar_station["properties"]["icao"]
                radar_station_name = primary_radar_station["properties"]["name"]
                message = f'{radar_station_name} radar.'
            elif self.get_radar_health(secondary_radar_station["properties"]["icao"]) == 'ok':
                radar_station_call = secondary_radar_station["properties"]["icao"]
                radar_station_name = secondary_radar_station["properties"]["name"]
                message = f'normally I would use the radar station in {primary_radar_station["properties"]["name"]} for you but it seems to be unavailable. falling back to {radar_station_name} radar.'
            else:
                radar_station_call = 'CONUS-LARGE'
                message = f'I checked two radar locations and they both seem to be offline. falling back to the continental us composite'
            radar_station_url = f"https://radar.weather.gov/ridge/standard/{radar_station_call}_loop.gif"
            radar_station_image = Image.open(io.BytesIO(requests.get(radar_station_url).content))
            radar_station_image.save("radar.gif", save_all=True)
            await ctx.send(message, file=discord.File("radar.gif"))
        except Exception as e:
            await ctx.send(f"error type: {type(e).__name__}, Error: {e}")

    @commands.command()
    async def forecast(self, ctx, location):
        """
        provide a US postal code and get the upcoming forecast
        """
        try:
            location = self.geolocator.geocode(location, exactly_one=True, country_codes='us')
            forecast_data, relative_name = self.get_forecast(
                f"{location.latitude},{location.longitude}")
            forecast_embed = self.format_forecast_embed(forecast_data, relative_name)
            return await ctx.send(embed=forecast_embed)
        except Exception as e:
            await ctx.send(f"error type: {type(e).__name__}, Error: {e}")

    # helper function to retrieve forecast data
    def get_forecast(self, location):
        # build URL for request
        url = f'https://api.weather.gov/points/{location}'
        headers = {'User-Agent': self.config['weather']['useragent']}
        # get data
        response = requests.get(url, headers=headers)
        data = response.json()
        # get forecast URL
        forecast_url = data['properties']['forecast']
        relative_name = f"{data['properties']['relativeLocation']['properties']['city']}, " \
                        f"{data['properties']['relativeLocation']['properties']['state']}"
        # get forecast data
        response = requests.get(forecast_url)
        forecast_data = response.json()
        return forecast_data, relative_name

    def get_radar_health(self, radar):
        # build URL for request
        url = f'https://api.weather.gov/radar/stations/{radar}'
        headers = {'User-Agent': self.config['weather']['useragent']}
        # get data
        response = requests.get(url, headers=headers)
        data = response.json()
        # get forecast URL
        last_receive_time = data['properties']['latency']['levelTwoLastReceivedTime']
        seconds_since_last_update = datetime.datetime.strptime(last_receive_time, '%Y-%m-%dT%H:%M:%S%z')
        tsss = datetime.datetime.now(datetime.timezone.utc) - seconds_since_last_update
        if tsss.total_seconds() > 600:
            health = 'bad'
        else:
            health = 'ok'
        return health

    # helper function to format forecast data as an embed
    @staticmethod
    def format_forecast_embed(forecast_data, relative_name):
        # get current forecast
        current_forecast = forecast_data['properties']['periods']
        # get embed title
        title = f"Forecast for {relative_name}"
        # get embed description
        description = f"Here is the upcoming forecast for {relative_name}"
        # create embed
        embed = discord.Embed(title=title, description=description, color=0x00ff00)
        embed.add_field(name=current_forecast[0]['name'], value=current_forecast[0]['detailedForecast'])
        embed.add_field(name=current_forecast[1]['name'], value=current_forecast[1]['detailedForecast'])
        embed.add_field(name=current_forecast[2]['name'], value=current_forecast[2]['detailedForecast'])
        embed.add_field(name=current_forecast[3]['name'], value=current_forecast[3]['detailedForecast'])
        embed.add_field(name=current_forecast[4]['name'], value=current_forecast[4]['detailedForecast'])
        embed.add_field(name=current_forecast[5]['name'], value=current_forecast[5]['detailedForecast'])
        embed.add_field(name=current_forecast[6]['name'], value=current_forecast[6]['detailedForecast'])
        embed.add_field(name=current_forecast[7]['name'], value=current_forecast[7]['detailedForecast'])
        embed.add_field(name=current_forecast[8]['name'], value=current_forecast[8]['detailedForecast'])
        return embed

    def get_radar_station(self, latitude, longitude):
        primary_radar_station = None
        primary_radar_station_distance = None
        secondary_radar_station = None
        secondary_radar_station_distance = None
        for station in self.radar_stations["features"]:
            station_latitude = station["geometry"]["coordinates"][0]
            station_longitude = station["geometry"]["coordinates"][1]
            station_distance = geodesic((latitude, longitude), (station_latitude, station_longitude)).miles
            if primary_radar_station_distance is None:
                primary_radar_station = station
                primary_radar_station_distance = station_distance
            elif station_distance < primary_radar_station_distance:
                secondary_radar_station = primary_radar_station
                primary_radar_station = station
                secondary_radar_station_distance = primary_radar_station_distance
                primary_radar_station_distance = station_distance
            elif station_distance < secondary_radar_station_distance:
                secondary_radar_station = station
                secondary_radar_station_distance = station_distance
        return primary_radar_station, secondary_radar_station

async def setup(bot):
    await bot.add_cog(Weather(bot))
