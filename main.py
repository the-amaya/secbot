import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)


startup_extensions = ["general", "management", "server_stuff"]


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
        await bot.start('token')

asyncio.run(main())
