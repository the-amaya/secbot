import discord
from discord.ext import commands


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog utilities is ready.')

    @commands.command()
    async def ping(self, ctx):
        """
        check the bot is responding as well as its latency
        """
        try:
            latency = self.bot.latency * 1000
        except:
            latency = '-latency-'
        await ctx.send(f'Pong! 🏓 {latency:.2f} ms')

    @commands.command()
    async def about(self, ctx):
        """
        Display the about info for the bot
        """
        embed = discord.Embed(title='About', color=discord.Colour.blue())
        embed.add_field(name='project home', value='https://github.com/the-amaya/secbot')
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utilities(bot))
