import discord
from discord.ext import commands
import asyncio
import configparser
import time
import os


def first_run():
    # check for the existence of the settings.ini file
    if not os.path.exists("settings.ini"):
        print(f"Welcome to secbot! We need to configure some settings before the bot can start. I will ask you for "
              f"each setting in the config file. the only setting absolutely required is the bot token.")

        # read the sample config from example_settings.ini using the configparser module
        first_run_config = configparser.ConfigParser()
        first_run_config.read('example_settings.ini')

        setting = input(f'your discord bot token')
        with setting:
            first_run_config.set('main_bot_settings', 'token', setting)

        setting = input(f'the command character you want to use or [enter] for default !')
        if setting:
            first_run_config.set('main_bot_settings', 'command_character', setting)

        setting = input(f'if you are using my sump pump project put its api url here. (you probably just want to hit '
                        f'[enter] here for none)')
        if setting:
            first_run_config.set('sump', 'sump_api_address', setting)

        setting = input(f"if you have a stable diffusion api running put its url here. example: "
                        f"'http://automatic1111.example.org:7860'")
        if setting:
            first_run_config.set('generate', 'api_url', setting)

        setting = input(f"if you want to use the weather cog you need to provide a user agent for the api calls. "
                        f"example: 'my discord bot me@example.com'")
        if setting:
            first_run_config.set('generate', 'api_url', setting)

        # present the updated config to the user for review
        for section in first_run_config.sections():
            print(f'*** {section.title()} ***')
            for key, value in first_run_config.items(section):
                print(f'{key} : {value}')

        # save updated config as settings.ini
        with open('settings.ini', 'w') as configfile:
            first_run_config.write(configfile)

        print('Settings saved successfully!')


first_run()


config = configparser.ConfigParser()
config.read('settings.ini')
command_character = config["main_bot_settings"]["command_character"]
token = config["main_bot_settings"]["token"]
intents = discord.Intents.all()
bot = commands.Bot(command_character, intents=intents)

startup_extensions = [
    "cogs.botsettings",
    "cogs.custom_reactions",
    "cogs.cute",
    "cogs.economy",
    "cogs.games",
    "cogs.loadunloadcogs",
    "cogs.stats",
    "cogs.utilities"
]


def optional_extensions():
    if os.path.exists("cameras.ini"):
        startup_extensions.append('cogs.cameras')
    if config["sump"]["sump_api_address"] != '':
        # need to check if that is actually an url
        startup_extensions.append('cogs.sump')
    if config["generate"]["api_url"] != '':
        # need to check if that is actually an url
        startup_extensions.append('cogs.generate')
    if config["weather"]["useragent"] != '':
        startup_extensions.append('cogs.weather')


optional_extensions()


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
