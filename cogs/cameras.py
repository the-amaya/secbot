import discord
from discord.ext import commands
from urllib.request import urlopen
from PIL import Image


# dict with friendly camera names and their IP

cameras = {
    'camera1': '10.0.0.11',
    'camera2': '10.0.0.12',
    'camera3': '10.0.0.13',
    'camera4': '10.0.0.14',
    'camera5': '10.0.0.15',
    'camera6': '10.0.0.16',
}

# TODO move the camera URL parts up here to variables to make it easier to use other cameras


class Cameras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog management is ready.')

    @commands.command(name='camera', help='View a still frame from one of the cameras')
    async def camera(self, ctx, cam='list'):
        async with ctx.typing():
            clist = list(cameras.keys())
            if cam == 'list':
                await ctx.send(f'valid cameras are: {clist}')
            elif cam in clist:
                try:
                    img_file = urlopen('http://' + cameras.get(
                        cam) + '/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=wuuPhkmUCeI9WG7C&user=user&password=password')
                    img = Image.open(img_file)
                    img.save('img.png')
                    await ctx.send(file=discord.File('img.png'))
                except Exception:
                    await ctx.send(f'something went wrong mate')
            else:
                await ctx.send(f'that is not a valid camera, please try again. valid cameras are {clist}')


async def setup(bot):
    await bot.add_cog(Cameras(bot))
