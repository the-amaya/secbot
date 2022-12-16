import discord
from discord.ext import commands
import random


class CuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog cute is ready.')

    @commands.command(name='ratecute', alias=['iscute'], help='Rate how cute a user is')
    async def ratecute(self, ctx, user: discord.User):
        """Rate how 'cute' a user is"""
        ratings = [
            'You are really really cute!',
            'You are so cute!',
            'You are pretty cute!',
            'You are kinda cute.',
            'You are not very cute...'
        ]

        await ctx.send(f'{user.mention} {ratings[random.randint(0, len(ratings) - 1)]}')


async def setup(bot):
    await bot.add_cog(CuteCog(bot))
