import discord
from discord.ext import commands
import sqlite3


class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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

    @commands.command()
    async def balance(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        self.c.execute("SELECT coins FROM coins WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, user.id))
        balance = self.c.fetchone()
        if balance is None:
            await ctx.send(f'{user.display_name} has no coins.')
        else:
            await ctx.send(f'{user.display_name} has {balance[0]} coins.')

    @commands.command()
    async def transfer(self, ctx, user: discord.Member, amount: int):
        # subtract coins from author
        self.c.execute("""
            INSERT INTO coins(guild_id, user_id, coins)
            VALUES(?,?,?) 
            ON CONFLICT(guild_id, user_id) 
            DO UPDATE SET coins = coins - ?
        """, (ctx.guild.id, ctx.author.id, -amount, amount))
        self.conn.commit()  # need to commit after every UPDATE operation

        # add coins to user
        self.c.execute("""
            INSERT INTO coins(guild_id, user_id, coins)
            VALUES(?,?,?) 
            ON CONFLICT(guild_id, user_id) 
            DO UPDATE SET coins = coins + ?
        """, (ctx.guild.id, user.id, amount, amount))
        self.conn.commit()  # need to commit after every UPDATE operation
        await ctx.send(f'{ctx.author.display_name} has given {user.display_name} {amount} coins.')

    @commands.command()
    async def earn(self, ctx, amount: int):
        # add coins to the author
        self.c.execute("""
            INSERT INTO coins(guild_id, user_id, coins)
            VALUES(?,?,?) 
            ON CONFLICT(guild_id, user_id) 
            DO UPDATE SET coins = coins + ?
        """, (ctx.guild.id, ctx.author.id, amount, amount))
        self.conn.commit()  # need to commit after every UPDATE operation
        await ctx.send(f'{ctx.author.display_name} has earned {amount} coins.')

    # commit changes and close connection when the bot exits
    def cog_unload(self):
        self.conn.commit()
        self.conn.close()


async def setup(bot):
    await bot.add_cog(Eco(bot))