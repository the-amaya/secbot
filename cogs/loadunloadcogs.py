import discord
from discord.ext import commands

# TODO command to list ALL cogs


class LoadUnloadCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog loadunloadcogs is ready.')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """
        load a cog. use dot path. e.g: cogs.loadunloadcogs
        """
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """
        unload a cog. use dot path. e.g: cogs.loadunloadcogs
        """
        try:
            await self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """
        reload a cog. will load a cog if not already loaded. use dot path. e.g: cogs.loadunloadcogs
        """
        try:
            await self.bot.unload_extension(cog)
        except discord.ext.commands.ExtensionNotLoaded:
            pass
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def list_cogs(self, ctx):
        """
        Lists all loaded cogs
        """
        # Get a list of all cogs
        all_cogs = [c.split(".")[0] for c in self.bot.cogs]
        # Send the list of all cogs
        await ctx.send(f"loaded cogs: {', '.join(all_cogs)}")


async def setup(bot):
    await bot.add_cog(LoadUnloadCogs(bot))
