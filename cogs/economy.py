import discord
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy_data = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog Economy is ready.')

    @commands.command(name='balance', help='Check your current balance')
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.economy_data:
            await ctx.send(f'{ctx.author.mention} has {self.economy_data[user_id]["balance"]} coins')
        else:
            self.economy_data[user_id] = {
                'balance': 0
            }
            await ctx.send(f'{ctx.author.mention} has 0 coins')

    @commands.command(name='transfer', help='transfer coins to another user. transfer <coins> <user>')
    async def transfer(self, ctx, amount: int, other: discord.User):
        user_id = str(ctx.author.id)
        other_id = str(other.id)
        if user_id in self.economy_data:
            if self.economy_data[user_id]["balance"] >= amount:
                if other_id in self.economy_data:
                    self.economy_data[user_id]["balance"] -= amount
                    self.economy_data[other_id]["balance"] += amount
                    await ctx.send(f'{ctx.author.mention} has transferred {amount} coins to {other.mention}')
                else:
                    self.economy_data[other_id] = {
                        'balance': amount
                    }
                    self.economy_data[user_id]["balance"] -= amount
                    await ctx.send(f'{ctx.author.mention} has transferred {amount} coins to {other.mention}')
            else:
                await ctx.send(f'{ctx.author.mention} does not have enough coins to transfer.')
        else:
            await ctx.send(f'{ctx.author.mention} does not have a balance.')

    @commands.command(name='earn', help='you can earn coins, simply specify the number you want!')
    async def earn(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        if user_id in self.economy_data:
            self.economy_data[user_id]["balance"] += amount
            await ctx.send(f'{ctx.author.mention} has earned {amount} coins.')
        else:
            self.economy_data[user_id] = {
                'balance': amount
            }
            await ctx.send(f'{ctx.author.mention} has earned {amount} coins.')


async def setup(bot):
    await bot.add_cog(Economy(bot))
