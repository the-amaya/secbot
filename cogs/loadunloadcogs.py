import discord
from discord.ext import commands


class LoadUnloadCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog loadunloadcogs is ready.')

    @commands.command(name='load', help='load a cog. use dot path. e.g: cogs.loadunloadcogs', hidden=True)
    async def load(self, ctx, *, cog: str):
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', help='unload a cog. use dot path. e.g: cogs.loadunloadcogs', hidden=True)
    async def unload(self, ctx, *, cog: str):
        try:
            await self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', help='reload a cog. use dot path. e.g: cogs.loadunloadcogs', hidden=True)
    async def _reload(self, ctx, *, cog: str):
        try:
            await self.bot.unload_extension(cog)
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


async def setup(bot):
    await bot.add_cog(LoadUnloadCogs(bot))
