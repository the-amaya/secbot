import discord
from discord.ext import commands
import asyncio
import configparser
import time

# dont change these values, go to settings.ini for all the user-configurable stuff

config = configparser.ConfigParser()
config.read('settings.ini')
command_character = config["main_bot_settings"]["command_character"]
token = config["main_bot_settings"]["token"]

intents = discord.Intents.all()
bot = commands.Bot(command_character, intents=intents)

startup_extensions = [
    "cogs.botsettings",
    #"cogs.cameras",
    "cogs.custom_reactions",
    "cogs.cute",
    "cogs.economy",
    "cogs.games",
    #"cogs.generate",
    "cogs.loadunloadcogs",
    "cogs.stats",
    #"cogs.sump",
    "cogs.utilities",
    "cogs.weather"
]


@bot.event
async def on_ready():
    bot.start_time = time.time()
    print('Bot is ready!')


async def load_extensions():
    for extension in startup_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())
