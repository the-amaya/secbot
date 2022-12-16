import discord
from discord.ext import commands


class BotSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog botsettings is ready.')

    @commands.command(name='setavatar', help='set the avatar for the bot (untested)', hidden=True)
    async def setavatar(self, ctx, *, avatar):
        # checks if user has permission to set the bot avatar
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("You do not have permission to set the bot's avatar.")
            return

        # sets the bot avatar
        try:
            with open(avatar, 'rb') as f:
                await self.bot.user.edit(avatar=f.read())
                await ctx.send(f"Successfully set the avatar to {avatar}.")
        except Exception as e:
            await ctx.send(f"There was an error setting the avatar: {e}")
            return

    @commands.command(name='setstatus', help='set the \'now playing\' status for the bot', hidden=True)
    async def setstatus(self, ctx, *, status):
        # checks if user has permission to set the bot status
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("You do not have permission to set the bot's status.")
            return

        # sets the bot status
        try:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=status))
            await ctx.send(f"Successfully set the status to {status}.")
        except Exception as e:
            await ctx.send(f"There was an error setting the status: {e}")
            return


async def setup(bot):
    await bot.add_cog(BotSettings(bot))
