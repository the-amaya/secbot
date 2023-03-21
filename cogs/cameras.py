import discord
from discord.ext import commands
from urllib.request import urlopen
from PIL import Image
import configparser
import os

# TODO the resizer function needs to be... better


class Cameras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_file_name = 'cameras.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file_name)
        self.cameras = {}
        for camera in self.config['cameras']:
            self.cameras.update({camera: self.config['cameras'][camera]})

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog management is ready.')

    @commands.command()
    async def camera(self, ctx, cam='list'):
        """
        View a still frame from one of the cameras.

        example camera <camera-name>
        to get a list of camera names, call 'camera list' or just 'camera'
        """
        async with ctx.typing():
            clist = list(self.cameras.keys())
            if cam == 'list':
                await ctx.send(f'valid cameras are: {clist}')
            elif cam in clist:
                try:
                    img_file = urlopen(f"{self.config['cameras_urlhelper']['prefix']}"
                                       f"{self.cameras.get(cam)}"
                                       f"{self.config['cameras_urlhelper']['postfix']}")
                    img = Image.open(img_file)
                    img.save('cam.png')
                    try:
                        self.check_compress_image('cam.png', int(8388608))
                    except:
                        await ctx.send(f'resizer error')
                    try:
                        await ctx.send(file=discord.File('cam.png'))
                    except discord.HTTPException as e:
                        await ctx.send(f"staus {e.status} response {e.response}")
                except Exception:
                    await ctx.send(f'something went wrong mate')
            else:
                await ctx.send(f'that is not a valid camera, please try again. valid cameras are {clist}')

    @staticmethod
    def check_compress_image(image_name, max_size):
        try:
            # Open the image
            image = Image.open(image_name)
            # Get the image size
            size = os.stat(image_name).st_size
            # If the size is greater than max_size, compress the image
            while size > max_size:
                # Compress the image
                image = image.reduce(2)
                # Save the compressed image
                image.save(image_name)
                # Get the compressed image size
                size = os.stat(image_name).st_size
            return
        except Exception as e:
            # Return the exception
            return e


async def setup(bot):
    await bot.add_cog(Cameras(bot))
