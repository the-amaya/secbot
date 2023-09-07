import discord
from discord.ext import commands
import sqlite3


class economyBackend:
    """this class provides economy functions that can be used in other cogs. should be something like
    from eco import economyBackend as db or something like that. see the command cog class below for
    usage examples. checkBalance returns an int or none, addBalance, subBalance and transfer will return
    true on success or false on failure. currently the only failure is insufficient funds"""
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

    def checkBalance(self, server: int, user: int) -> int | None:
        self.c.execute("SELECT coins FROM coins WHERE guild_id = ? AND user_id = ?", (server, user))
        balance = self.c.fetchone()
        return balance[0]

    def addBalance(self, server: int, user: int, amount: int) -> bool:
        # add coins to user
        self.c.execute("""
                    INSERT INTO coins(guild_id, user_id, coins)
                    VALUES(?,?,?) 
                    ON CONFLICT(guild_id, user_id) 
                    DO UPDATE SET coins = coins + ?
                """, (server, user, amount, amount))
        self.conn.commit()  # need to commit after every UPDATE operation
        return True

    def subBalance(self, server: int, user: int, amount: int) -> bool:
        # subtract coins from specified user
        # returns false on insufficent funds
        # start by checking the balance
        bal = self.checkBalance(server, user)
        if amount > bal:
            # insufficent funds
            return False
        else:
            self.c.execute("""
                          INSERT INTO coins(guild_id, user_id, coins)
                          VALUES(?,?,?) 
                          ON CONFLICT(guild_id, user_id) 
                          DO UPDATE SET coins = coins - ?
                          """, (server, user, -amount, amount))
            self.conn.commit()  # need to commit after every UPDATE operation\
            return True

    def transfer(self, server: int, fromUser: int, toUser: int, amount: int) -> bool:
        if self.subBalance(server, fromUser, amount):
            self.addBalance(server, toUser, amount)
            return True
        else:
            return False


class Eco(commands.Cog):
    """The basic economy functions"""
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
        if self.db.transfer(ctx.guild.id, ctx.author.id, user.id, amount):
            await ctx.send(f'{ctx.author.display_name} has given {user.display_name} {amount} coins.')
        else:
            await ctx.send(f'{ctx.author.display_name} does not have enough coins to give {amount} to '
                           f'{user.display_name}. You can check your balance with the balance command')

    @commands.command(name='earn', help='you can earn coins, simply specify the number you want!')
    async def earn(self, ctx, amount: int):
        if self.db.addBalance(ctx.guild.id, ctx.author.id, amount):
            balance = self.db.checkBalance(ctx.guild.id, ctx.author.id)
            await ctx.send(f'{ctx.author.display_name} has earned {amount} coins. Your new balance is {balance}')
        else:
            await ctx.send(f'I am sorry, but I was unable to add coins to your balance for some reason, sorry about '
                           f'that {ctx.author.display_name}, maybe try again or @ the bot owner')


async def setup(bot):
    await bot.add_cog(Eco(bot))
