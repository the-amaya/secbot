import discord
from discord.ext import commands
import drivewatch

server_list = list(drivewatch.serverlist.keys())

class Server_Stuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='servers', help=f'print a physical layout of drives for each server with temp and '
                                         f'racsec count. currently available for the following servers: '
                                         f'{list(drivewatch.serverlist.keys())}')
    async def servers(self, ctx):
        async with ctx.typing():
            await ctx.send(await drivewatch.trinity_table())
        async with ctx.typing():
            await ctx.send(await drivewatch.backup_table())


    @commands.command(name='racsec', help='get a list of drives with reallocated sectors on a specified server')
    async def racsec(self, ctx, server=''):
        async with ctx.typing():
            if server in server_list:
                await ctx.send(await drivewatch.reallocated_sectors(server))
            elif server == '':
                await ctx.send(f'this command requires a server, valid servers are {server_list}')
            else:
                await ctx.send(f'valid servers are: {server_list}')


    @commands.command(name='badarray', help='get a list of non-OK arrays from all the servers')
    async def badarray(self, ctx):
        async with ctx.typing():
            await ctx.send(await drivewatch.all_status())


    @commands.command(name='baddrive', help='get a list of non-OK drives from one of the servers')
    async def baddrive(self, ctx, server=''):
        async with ctx.typing():
            if server in server_list:
                await ctx.send(await drivewatch.drive_status(server))
            elif server == '':
                await ctx.send(f'this command requires a server, valid servers are {server_list}')
            else:
                await ctx.send(f'valid servers are: {server_list}')

async def setup(bot):
    await bot.add_cog(Server_Stuff(bot))
