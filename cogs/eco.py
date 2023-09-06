import discord
from discord.ext import commands
import sqlite3


class economyBackend():
    def __init__(self):
        self.conn = sqlite3.connect('economy.db')
        self.c = self.conn.cursor()

        # creating table for coins if not exist
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS coins (
            guild_id INT,
            user_id INT,
            coins INT,
            PRIMARY KEY (guild_id, user_id))
        """)

    def checkBalance(self, server, user):
        self.c.execute("SELECT coins FROM coins WHERE guild_id = ? AND user_id = ?", (server, user))
        balance = self.c.fetchone()
        return balance[0]

    def addBalance(self, server, user, amount):
        # add coins to user
        self.c.execute("""
                    INSERT INTO coins(guild_id, user_id, coins)
                    VALUES(?,?,?) 
                    ON CONFLICT(guild_id, user_id) 
                    DO UPDATE SET coins = coins + ?
                """, (server, user, amount, amount))
        self.conn.commit()  # need to commit after every UPDATE operation

    def subBalance(self, server, user, amount):
        # subtract coins from author
        self.c.execute("""
                    INSERT INTO coins(guild_id, user_id, coins)
                    VALUES(?,?,?) 
                    ON CONFLICT(guild_id, user_id) 
                    DO UPDATE SET coins = coins - ?
                """, (server, user, -amount, amount))
        self.conn.commit()  # need to commit after every UPDATE operation

    def transfer(self, server, fromUser, toUser, amount):
        self.subBalance(server, fromUser, amount)
        self.addBalance(server, toUser, amount)


class Eco(commands.Cog):
    "The basic economy functions"
    def __init__(self, bot):
        self.bot = bot
        self.db = economyBackend()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog Eco is ready.')

    @commands.command(name='balance', help='Check your current balance')
    async def balance(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        balance = self.db.checkBalance(ctx.guild.id, user.id)
        if balance is None:
            await ctx.send(f'{user.display_name} has no coins.')
        else:
            await ctx.send(f'{user.display_name} has {balance} coins.')

    @commands.command(name='transfer', help='transfer coins to another user. transfer <coins> <user>')
    async def transfer(self, ctx, user: discord.Member, amount: int):
        self.db.subBalance(ctx.guild.id, ctx.author.id, amount)
        self.db.addBalance(ctx.guild.id, user.id, amount)
        await ctx.send(f'{ctx.author.display_name} has given {user.display_name} {amount} coins.')

    @commands.command(name='earn', help='you can earn coins, simply specify the number you want!')
    async def earn(self, ctx, amount: int):
        self.db.addBalance(ctx.guild.id, ctx.author.id, amount)
        balance = self.db.checkBalance(ctx.guild.id, ctx.author.id)
        await ctx.send(f'{ctx.author.display_name} has earned {amount} coins. Your new balance is {balance}')


async def setup(bot):
    await bot.add_cog(Eco(bot))
