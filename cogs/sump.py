import discord
from discord.ext import commands
import requests
import configparser

# TODO test
# TODO add try/except for the api call?


class Sump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_file_name = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file_name)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog sump is ready.')

    @commands.command()
    async def sumpdata(self, ctx):
        """
        this command will query the api of my sump-pump project and return info
        for more information about the sump pump project see https://github.com/the-amaya/sumpPump
        that is likely an old version that does not have the API, I will eventually post an update
        if this is a functionality that  you actively want open an issue on github
        """
        # query the API to get the data
        r = requests.get(self.config["sump"]["sump_api_address"])
        data = r.text.split('_')
        # parse the data
        count = data[0]
        lrt = data[1]
        tslr = data[2]
        rph = data[3]
        rpd = data[4]
        level = data[5]
        # format the response
        response = f"The sump pump has run {count} times. " \
                   f"The last time it ran was {lrt}. " \
                   f"It has been {tslr} since then. " \
                   f"The average times it runs per hour is {rph} " \
                   f"and the average times it runs per day is {rpd}. " \
                   f"The current water level is {level} cm."

        # send the response
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(Sump(bot))
