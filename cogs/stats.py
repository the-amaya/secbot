import discord
from discord.ext import commands
import time
import sqlite3

# TODO ping needs moved out of this cog. maybe into a utility cog
# TODO fix the user stats to be per-server
# TODO what is @staticmethod and should i be using it elsewhere?

conn = sqlite3.connect('stats.db')
c = conn.cursor()
# Create the stats table if it does not exist
c.execute("""CREATE TABLE IF NOT EXISTS stats (
    user_id TEXT UNIQUE,
    messages_sent INTEGER DEFAULT 0,
    reactions_given INTEGER DEFAULT 0,
    reactions_received INTEGER DEFAULT 0,
    attachments_sent INTEGER DEFAULT 0
)""")
c.execute("""CREATE TABLE IF NOT EXISTS server_stats (
    server_id TEXT UNIQUE,
    messages_sent INTEGER DEFAULT 0
)""")


class Stats(commands.Cog):
    "this cog tracks and allows you to view user and bot stats."
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog stats is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        # Increment the number of messages sent in the server
        c.execute("INSERT INTO server_stats (server_id, messages_sent) VALUES (?, ?) ON CONFLICT(server_id) "
                  "DO UPDATE SET messages_sent = server_stats.messages_sent + 1", (message.guild.id, 1))
        conn.commit()
        c.execute("INSERT INTO stats (user_id, messages_sent, attachments_sent) "
                  "VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET "
                  "messages_sent = stats.messages_sent + 1, attachments_sent = stats.attachments_sent + ?",
                  (message.author.id, 1, len(message.attachments), len(message.attachments))
                  )
        conn.commit()

    @commands.command(name='user_stats', help='print stats for yourself or another user')
    async def user_stats(self, ctx, user: discord.User = None):
        user = ctx.author if not user else user
        # Get the message count and other stats for the user
        c.execute("SELECT * FROM stats WHERE user_id = ?", (user.id,))
        result = c.fetchone()
        # Format the stats
        stats_embed = discord.Embed(title="User Statistics", description=f"{user.name}'s Stats", color=0x00ff00)
        stats_embed.add_field(name="Messages Sent", value=result[1])
        await ctx.send(embed=stats_embed)

    @commands.command(name='ping', help='check the bot is responding as well as its latency')
    async def ping(self, ctx):
        try:
            latency = self.bot.latency * 1000
        except:
            latency = '-latency-'
        await ctx.send(f'Pong! 🏓 {latency:.2f} ms')

    @commands.command(name='botstats')
    async def botstats(self, ctx):
        """Display bot statistics"""
        guilds = len(self.bot.guilds)
        members = len(list(self.bot.get_all_members()))
        channels = len([c for c in self.bot.get_all_channels()])
        uptime = await self.pretty_time_delta(time.time() - self.bot.start_time)
        latency = self.bot.latency * 1000
        # Display stats
        embed = discord.Embed(title='Bot Statistics', color=discord.Colour.blue())
        embed.add_field(name='Guilds', value=guilds)
        embed.add_field(name='Members', value=members)
        embed.add_field(name='Channels', value=channels)
        embed.add_field(name='Uptime', value=uptime)
        embed.add_field(name='Latency', value=f'{latency:.2f} ms')
        await ctx.send(embed=embed)

    @commands.command(name='about')
    async def about(self, ctx):
        """
        Display the about info for the bot
        """
        embed = discord.Embed(title='About', color=discord.Colour.blue())
        embed.add_field(name='project home', value='https://github.com/the-amaya/secbot')
        await ctx.send(embed=embed)

    @staticmethod
    async def pretty_time_delta(seconds):
        seconds = int(seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return '%dd%dh%dm%ds' % (days, hours, minutes, seconds)
        elif hours > 0:
            return '%dh%dm%ds' % (hours, minutes, seconds)
        elif minutes > 0:
            return '%dm%ds' % (minutes, seconds)
        else:
            return '%ds' % (seconds,)


async def setup(bot):
    await bot.add_cog(Stats(bot))
