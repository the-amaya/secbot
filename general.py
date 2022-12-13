import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('stats.db')
c = conn.cursor()
# Create the stats table if it does not exist
c.execute("""CREATE TABLE IF NOT EXISTS stats (
    key INTEGER PRIMARY KEY,
    user_id TEXT UNIQUE,
    messages_sent INTEGER DEFAULT 0
)""")

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message, bot):
        # Increment the number of messages sent by the user
        c.execute("INSERT INTO stats (user_id, messages_sent) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET "
                  "messages_sent = stats.messages_sent + 1", (message.author.id, 1))
        conn.commit()
        await bot.process_commands(message)

    @commands.command(name='stats', help='View user statistics')
    @commands.has_permissions(send_messages=True)
    async def stats(self, ctx):
        """returns user stats, currently accepts no arguments and only replys for self"""
        # Get the user's stats
        c.execute("SELECT * FROM stats WHERE user_id = ?", (ctx.author.id,))
        result = c.fetchone()
        # If the user has no stats, create a new record
        if result is None:
            c.execute("INSERT INTO stats (user_id) VALUES (?)", (ctx.author.id,))
            conn.commit()
            # Get the user's stats
            c.execute("SELECT * FROM stats WHERE user_id = ?", (ctx.author.id,))
            result = c.fetchone()
        # Format the stats
        stats_embed = discord.Embed(title="User Statistics", description=f"{ctx.author.name}'s Stats", color=0x00ff00)
        stats_embed.add_field(name="Messages Sent", value=result[2])
        await ctx.send(embed=stats_embed)

    @stats.error
    async def stats_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send(text)

async def setup(bot):
    await bot.add_cog(General(bot))
