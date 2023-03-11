import discord
import pgeocode
from urllib.request import urlopen
from discord.ext import commands
from PIL import Image
import numpy
import requests

# TODO better embed formatting. maybe build a graph or something for the forecast
# TODO it takes *forever* to chug through the whole list of radar locations looking for the closest.
#  need a better solution, also need a better solution than the mess that follows...
# TODO add regional radar locations

# TODO I think the solution is to use lat,long and pythagorean theorem
# TODO we should also accept a callsign and just return that radar loop.
#  probably implement when we implement the regions

radar_list = [['KABR', "ABERDEEN,  SD", '57401'],
              ['KBIS', "BISMARCK,  ND", '58501'],
              ['KFTG', "FRONT RANGE AP,  CO", '80022'],
              ['KDMX', "JOHNSTON,  IA", '50131'],
              ['KDTX', "WHITE LAKE,  MI", '48383'],
              ['KDDC', "DODGE CITY,  KS", '67801'],
              ['KDLH', "DULUTH,  MN", '55802'],
              ['KCYS', "CHEYENNE,  WY", '82001'],
              ['KLOT', "ROMEOVILLE,  IL", '60446'],
              ['KGLD', "GOODLAND,  KS", '67735'],
              ['KUEX', "BLUE HILL,  NE", '68930'],
              ['KGJX', "GRAND JUNCTION,  CO", '81501'],
              ['KGRR', "GRAND RAPIDS,  MI", '49501'],
              ['KMVX', "GRAND FORKS,  ND", '58201'],
              ['KGRB', "GREEN BAY,  WI", '54301'],
              ['KIND', "INDIANAPOLIS,  IN", '46201'],
              ['KJKL', "JACKSON,  KY", '41339'],
              ['KARX', "LA CROSSE,  WI", '54601'],
              ['KILX', "LINCOLN,  IL", '62656'],
              ['KLVX', "FORT KNOX,  KY", '40121'],
              ['KMQT', "NEGAUNEE,  MI", '49866'],
              ['KMKX', "DOUSMAN,  WI", '53118'],
              ['KMPX', "CHANHASSEN,  MN", '55317'],
              ['KAPX', "GAYLORD,  MI", '49735'],
              ['KLNX', "NORTH PLATTE,  NE", '69101'],
              ['KIWX', "NORTH WEBSTER,  IN", '46555'],
              ['KOAX', "VALLEY,  NE", '68064'],
              ['KPAH', "PADUCAH,  KY", '42001'],
              ['KEAX', "PLEASANT HILL,  MO", '64080'],
              ['KPUX', "PUEBLO,  CO", '81001'],
              ['KDVN', "DAVENPORT,  IA", '52801'],
              ['KUDX', "NEW UNDERWOOD,  SD", '57761'],
              ['KRIW', "RIVERTON,  WY", '82501'],
              ['KSGF', "SPRINGFIELD,  MO", '65801'],
              ['KLSX', "WELDON SPRING,  MO", '63304'],
              ['KFSD', "SIOUX FALLS,  SD", '57101'],
              ['KTWX', "TOPEKA,  KS", '66601'],
              ['KICT', "WICHITA,  KS", '67201'],
              ['KVWX', "OWENSVILLE,  IN", '47665'],
              ['KLTX', "SHALLOTTE,  NC", '28459'],
              ['KCCX', "STATE COLLEGE,  PA", '16801'],
              ['KLWX', "STERLING,  VA", '20163'],
              ['KFCX', "ROANOKE,  VA", '24001'],
              ['KRAX', "CLAYTON,  NC", '27520'],
              ['KGYX', "GRAY,  ME", '04039'],
              ['KDIX', "FORT DIX,  NJ", '08640'],
              ['KPBZ', "CORAOPOLIS,  PA", '15108'],
              ['KAKQ', "WAKEFIELD,  VA", '23888'],
              ['KMHX', "NEWPORT,  NC", '28570'],
              ['KGSP', "GREER,  SC", '29650'],
              ['KILN', "WILMINGTON,  OH", '45177'],
              ['KCLE', "CLEVELAND,  OH", '44101'],
              ['KCAE', "WEST COLUMBIA,  SC", '29169'],
              ['KBGM', "BINGHAMTON,  NY", '13901'],
              ['KENX', "EAST BERNE,  NY", '12059'],
              ['KBUF', "BUFFALO,  NY", '14201'],
              ['KCXX', "COLCHESTER,  VT", '05439'],
              ['KCBW', "HOULTON,  ME", '04730'],
              ['KBOX', "TAUNTON,  MA", '02780'],
              ['KOKX', "UPTON,  NY", '11973'],
              ['KCLX', "GRAYS,  SC", '29666'],
              ['KRLX', "CHARLESTON,  WV", '25301'],
              ['KBRO', "BROWNSVILLE,  TX", '78520'],
              ['KABX', "ALBUQUERQUE,  NM", '87101'],
              ['KAMA', "AMARILLO,  TX", '79101'],
              ['KFFC', "PEACHTREE CITY,  GA", '30269'],
              ['KEWX', "NEW BRAUNFELS,  TX", '78130'],
              ['KBMX', "ALABASTER,  AL", '35007'],
              ['KCRP', "CORPUS CHRISTI,  TX", '78401'],
              ['KFWS', "FORT WORTH,  TX", '76101'],
              ['KEPZ', "SANTA TERESA,  NM", '88008'],
              ['KHGX', "DICKINSON,  TX", '77539'],
              ['KJAX', "JACKSONVILLE,  FL", '32099'],
              ['KBYX', "BOCA CHICA KEY,  FL", '33040'],
              ['KMRX', "MORRISTOWN,  TN", '37813'],
              ['KLBB', "LUBBOCK,  TX", '79401'],
              ['KLZK', "NORTH LITTLE ROCK,  AR", '72113'],
              ['KLCH', "LAKE CHARLES,  LA", '70601'],
              ['KOHX', "OLD HICKORY,  TN", '37138'],
              ['KMLB', "MELBOURNE,  FL", '32901'],
              ['KNQA', "MILLINGTON,  TN", '38053'],
              ['KAMX', "MIAMI,  FL", '33101'],
              ['KMAF', "MIDLAND,  TX", '79701'],
              ['KTLX', "OKLAHOMA CITY,  OK", '73101'],
              ['KHTX', "HYTOP,  AL", '35768'],
              ['KMOB', "MOBILE,  AL", '36601'],
              ['KTLH', "TALLAHASSEE,  FL", '32301'],
              ['KTBW', "RUSKIN,  FL", '33570'],
              ['KSJT', "SAN ANGELO,  TX", '76901'],
              ['KINX', "INOLA,  OK", '74036'],
              ['KSRX', "CHAFFEE RIDGE,  AR", '72086'],
              ['KLIX', "SLIDELL,  LA", '70458'],
              ['KDGX', "BRANDON,  MS", '39042'],
              ['KSHV', "SHREVEPORT,  LA", '71101'],
              ['KLGX', "LANGLEY HILL,  WA", '98039'],
              ['KOTX', "SPOKANE,  WA", '99201'],
              ['KEMX', "TUCSON,  AZ", '85701'],
              ['KYUX', "YUMA,  AZ", '85364'],
              ['KNKX', "SAN DIEGO,  CA", '92101'],
              ['KMUX', "LOS GATOS,  CA", '95030'],
              ['KHNX', "HANFORD,  CA", '93230'],
              ['KSOX', "SANTA ANA MOUNTAINS,  CA", '92676'],
              ['KATX', "EVERETT,  WA", '98201'],
              ['KIWA', "PHOENIX,  AZ", '85001'],
              ['KRTX', "PORTLAND,  OR", '97086'],
              ['KSFX', "SPRINGFIELD,  ID", '83277'],
              ['KRGX', "NIXON,  NV", '89424'],
              ['KDAX', "DAVIS,  CA", '95616'],
              ['KMTX', "SALT LAKE CITY,  UT", '84101'],
              ['KPDT', "PENDLETON,  OR", '97801'],
              ['KMSX', "MISSOULA,  MT", '59801'],
              ['KESX', "LAS VEGAS,  NV", '89101'],
              ['KVTX', "LOS ANGELES,  CA", '90001'],
              ['KMAX', "MEDFORD,  OR", '97501'],
              ['KFSX', "FLAGSTAFF,  AZ", '86001'],
              ['KGGW', "GLASGOW,  MT", '59230'],
              ['KLRX', "ELKO,  NV", '89801'],
              ['KBHX', "EUREKA,  CA", '95501'],
              ['KTFX', "GREAT FALLS,  MT", '59401'],
              ['KCBX', "BOISE,  ID", '83701'],
              ['KBLX', "BILLINGS,  MT", '59101'],
              ['KICX', "CEDAR CITY,  UT", '84720'],
              ['PABC', "ANCHORAGE,  AK", '99501'],
              ['PAPD', "FAIRBANKS,  AK", '99701'],
              ['PHKM', "HONOLULU,  HI", '96801'],
              ['PAHG', "ANCHORAGE,  AK", '99504'],
              ['PAKC', "ANCHORAGE,  AK", '99516'],
              ['PAIH', "ANCHORAGE,  AK", '99507'],
              ['PHMO', "HONOLULU,  HI", '96850'],
              ['PAEC', "FAIRBANKS,  AK", '99709'],
              ['TJUA', "SAN JUAN,  PR", '00901'],
              ['PACG', "JUNEAU,  AK", '99801'],
              ['PHKI', "HONOLULU,  HI", '96813'],
              ['PHWA', "HONOLULU,  HI", '96817'],
              ['KFDR', "NORMAN,  OK", '73019'],
              ['PGUA', "AGANA,  GU", '96910'],
              ['KBBX', "SACRAMENTO,  CA", '94203'],
              ['KFDX', "ALBUQUERQUE,  NM", '87101'],
              ['KGWX', "JACKSON,  MS", '39201'],
              ['KDOX', "WAKEFIELD,  VA", '23888'],
              ['KDYX', "SAN ANGELO,  TX", '76901'],
              ['KEYX', "LAS VEGAS,  NV", '89101'],
              ['KEVX', "MOBILE,  AL", '36601'],
              ['KHPX', "PADUCAH,  KY", '42001'],
              ['KTYX', "SOUTH BURLINGTON,  VT", '05403'],
              ['KGRK', "FORT WORTH,  TX", '76101'],
              ['KPOE', "LAKE CHARLES,  LA", '70601'],
              ['KEOX', "TALLAHASSEE,  FL", '32301'],
              ['KHDX', "SANTA TERESA,  NM", '88008'],
              ['KDFX', "NEW BRAUNFELS,  TX", '78130'],
              ['KMXX', "ALABASTER,  AL", '35007'],
              ['KMBX', "BISMARCK,  ND", '58501'],
              ['KVAX', "JACKSONVILLE,  FL", '32099'],
              ['KJGX', "PEACHTREE CITY,  GA", '30269'],
              ['KVNX', "NORMAN,  OK", '73019']
              ]


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog weather is ready.')

    @commands.command()
    async def radar(self, ctx, postal_code=''):
        """
        provide a US postal code to get the current radar image for that area
        """
        if postal_code == '':
            return await ctx.send("Please provide a US postal code to search for the nearest radar station.")
        else:
            user_location = pgeocode.Nominatim('us').query_postal_code(postal_code)
            if numpy.isnan(user_location['accuracy']):
                return await ctx.send("Please provide a valid US zip code.")
            else:
                min_distance = -1
                best_match = ""
                for station in radar_list:
                    distcode = pgeocode.GeoDistance('us')
                    distance = distcode.query_postal_code(user_location['postal_code'], station[2])
                    if min_distance == -1 or min_distance > distance:
                        min_distance = distance
                        best_match = station[0]
                        best_match_loc = station[1]
                radar_url = f"https://radar.weather.gov/ridge/standard/{best_match}_loop.gif"
                try:
                    img_file = urlopen(radar_url)
                    img = Image.open(img_file)
                    img.save('radar.gif', save_all=True)
                    inbed = discord.Embed(title=f"{best_match}",
                                          description=f"the radar located in {best_match_loc} was the closest I could "
                                                      f"find to you",
                                          color=0x020202)
                    rfile = discord.File("radar.gif", filename="radar.gif")
                    inbed.set_image(url='attachment://radar.gif')
                    return await ctx.reply(file=rfile, embed=inbed)
                except Exception:
                    await ctx.send(f'something went wrong mate')

    # command to retrieve forecast from NWS API
    @commands.command()
    async def forecast(self, ctx, postal_code=''):
        """
        provide a US postal code and get the upcoming forecast
        """
        if postal_code == '':
            return await ctx.send("Please provide a US postal code to get the forecast.")
        else:
            user_location = pgeocode.Nominatim('us').query_postal_code(postal_code)
            if numpy.isnan(user_location['accuracy']):
                return await ctx.send("Please provide a valid US zip code.")
            else:
                pass
        # get forecast from NWS
        try:
            forecast_data, relative_name = self.get_forecast(
                f"{user_location['latitude']},{user_location['longitude']}")
        except:
            return await ctx.send('unable to get the forecast data')
        # format data as an embed
        try:
            forecast_embed = self.format_forecast_embed(forecast_data, relative_name)
        except Exception as e:
            return await ctx.send(f'unable to format the embed. {type(e).__name__}')
        # send embed to user
        try:
            return await ctx.send(embed=forecast_embed)
        except:
            return await ctx.send('something went wrong mate')

    # helper function to retrieve forecast data
    @staticmethod
    def get_forecast(location):
        # build URL for request
        url = f'https://api.weather.gov/points/{location}'
        headers = {'User-Agent': 'secbot, a discord bot. https://github.com/the-amaya/secbot'}
        # get data
        response = requests.get(url, headers=headers)
        data = response.json()
        # get forecast URL
        forecast_url = data['properties']['forecast']
        relative_name = f"{data['properties']['relativeLocation']['properties']['city']}, {data['properties']['relativeLocation']['properties']['state']}"
        # get forecast data
        response = requests.get(forecast_url)
        forecast_data = response.json()
        return forecast_data, relative_name

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


async def setup(bot):
    await bot.add_cog(Weather(bot))
