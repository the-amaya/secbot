import discord
from discord.ext import commands
import configparser

# TODO the edit settings command doesnt work, setavatar is still untested


class BotSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_file_name = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file_name)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog botsettings is ready.')

    @commands.command()
    @commands.is_owner()
    async def setavatar(self, ctx, *, avatar):
        """
        set the avatar for the bot (untested)
        """
        # sets the bot avatar
        try:
            with open(avatar, 'rb') as f:
                await self.bot.user.edit(avatar=f.read())
                await ctx.send(f"Successfully set the avatar to {avatar}.")
        except Exception as e:
            await ctx.send(f"There was an error setting the avatar: {e}")
            return

    @commands.command()
    @commands.is_owner()
    async def setstatus(self, ctx, *, status):
        """
        set the 'now playing' status for the bot
        """
        try:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=status))
            await ctx.send(f"Successfully set the status to {status}.")
        except Exception as e:
            await ctx.send(f"There was an error setting the status: {e}")
            return

    @commands.command()
    @commands.is_owner()
    async def view_settings(self, ctx):
        """
        View settings stored in the settings.ini file
        """
        settings_string = ""
        for section in self.config.sections():
            settings_string += f"\n[{section}]\n"
            for setting in self.config[section]:
                settings_string += f"{setting}={self.config[section][setting]}\n"
        if ctx.guild is None:
            await ctx.send(f"```{settings_string}```")
        else:
            try:
                await ctx.author.send(f"```{settings_string}```")
            except discord.Forbidden:
                await ctx.send(f"you are not accepting DMs so I was unable to message you. fix that and try again")

    @commands.command()
    @commands.is_owner()
    async def edit_setting(self, ctx, section, setting, value):
        """
        Edit a setting in the settings.ini file (currently not functional)
        sorry, edit it manually for now :(
        """
        self.config[section][setting] = value
        with open(self.settings_file_name, 'w') as configfile:
            self.config.write(configfile)
        if ctx.guild is None:
            await ctx.send(f"Successfully set {setting} to {value} in {section}")
        else:
            try:
                await ctx.author.send(f"Successfully set {setting} to {value} in {section}")
            except discord.Forbidden:
                await ctx.send(f"you are not accepting DMs so I was unable to message you. fix that and try again")


async def setup(bot):
    await bot.add_cog(BotSettings(bot))
