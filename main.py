import discord
from discord.ext import commands
import asyncio
import configparser
import time

# dont change these values, go to settings.ini for all the user-configurable stuff
config = configparser.ConfigParser()
config.read('settings.ini')
command_character = config["main bot settings"]["command_character"]
token = config["main bot settings"]["token"]

intents = discord.Intents.all()
bot = commands.Bot(command_character, intents=intents)

startup_extensions = [
    "cogs.cameras",
    "cogs.serverstuff",
    "cogs.loadunloadcogs",
    "cogs.botsettings",
    "cogs.cute",
    "cogs.economy",
    "cogs.games",
    "cogs.stats"
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
