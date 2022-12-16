import discord
from discord.ext import commands
import random


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog games is ready.')

    @commands.command(name='8ball', aliases=['eight_ball', 'eightball', '8_ball'], help='ask the 8ball a question')
    async def eight_ball(self, ctx):
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.',
        ]
        await ctx.send(f'Question: {ctx.message.content}\nAnswer: {random.choice(responses)}')


async def setup(bot):
    await bot.add_cog(Games(bot))
