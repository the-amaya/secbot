import aiohttp
import discord
from discord.ext import commands
from PIL import Image
import io
import asyncio
import base64
import json
import configparser
import random

# TODO move the image generation settings to the settings file
# TODO move the API call (and embed building) into its own function
# TODO add request logging

opssec = 300000
opcost = 0.000003
maxcost = 10000000000

status_gifs = ['status_anvil.gif',
               'status_calculations.gif',
               'status_computer.gif',
               'status_mouse.gif',
               'status_tv.gif']


class GenerateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_file_name = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file_name)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog generate is ready.')

    @commands.command()
    async def generate(
            self,
            ctx,
            prompt: str = commands.parameter(description="The prompt to use for generation"),
            steps: int = commands.parameter(default="25", description="the number of steps for the generator to use"),
            scale: float = commands.parameter(default="12.5", description=f"prompt factor, normal range 0-30 "
                                                                          f"but will take other values"),
            width: int = commands.parameter(default="512", description="image width"),
            height: int = commands.parameter(default="512", description="image height"),
            negative: str = commands.parameter(default="", description="the negative prompt"),
            seed: str = commands.parameter(default="-1",
                                           description="seed to use for generation. leave default for random")
    ):
        """Generate an image from a privately hosted stable diffusion API, accepts additional arguments.

        examples: !generate puppy !generate "tall drink of water" 30 !generate "big image with a lot of steps that
        will take a while" 150 12.5 2048 2048 "negative prompt here" 2943943922384575

        parameters with a default value are optional but must be specified in order (if you want to specify scale you
        must specify steps first)


        see also the `gen` command
        """

        params = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": scale,
            "negative_prompt": negative,
            "seed": seed,
            "sampler_index": "Euler a"
        }

        width, height, steps = int(width), int(height), int(steps)
        if width <= 512 and height <= 512:
            weight = 1
        elif width <= 1024 and height <= 1024:
            weight = 2
        elif width <= 2048 and height <= 2048:
            weight = 4
        else:
            weight = 8

        maxsize = 2560000
        reqsize = width * height
        if reqsize > maxsize:
            return await ctx.send(
                f'that image size is probably too big for the available ram. try a lower resolution (max resolution '
                f'set at 1600x1600 or a combination thereof')

        cost = width * height * steps * weight
        estrt = cost / opssec
        notecleanup = 0
        if cost > maxcost:
            return await ctx.send(
                f'that combination of steps and size is too expensive, try reducing the width, heigth and/or number '
                f'of steps')
        if estrt > 60:
            tembed = discord.Embed(title="this is gonna take a moment",
                                   description=f'the estimated gentime is {self.pretty_time_delta(estrt)}',
                                   color=0xBDB76B)
            tfile = discord.File("assets/loading.gif", filename="loading.gif")
            tembed.set_thumbnail(url="attachment://loading.gif")
            timenotice = await ctx.send(file=tfile, embed=tembed)
            notecleanup = 1

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.config['generate']['api_url']}/sdapi/v1/txt2img", json=params,
                                    timeout=-1) as resp:
                if resp.status != 200:
                    await self.error_embed(ctx, 'API error', f'the response status was not ok. response: {resp.status}')
                if notecleanup == 1:
                    await timenotice.delete()
                data = await resp.json()
                try:
                    for i in data['images']:
                        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
                        image.save('img.png')
                        inbed = discord.Embed(title="Generated image", description=prompt, color=0xBA55D3)
                        gfile = discord.File("img.png", filename="img.png")
                        inbed.set_image(url='attachment://img.png')
                        info = json.loads(data['info'])
                        runtime = resp.headers['x-process-time']
                        runtime = runtime.strip()
                        runtime = float(runtime)
                        runtime = round(runtime)
                        if runtime > estrt:
                            rtt = f"I underestimated by {self.pretty_time_delta(runtime - estrt)}"
                        else:
                            rtt = f"I overestimated by {self.pretty_time_delta(estrt - runtime)}"
                        inbed.set_footer(text=f"seed: {info['seed']} runtime: {self.pretty_time_delta(runtime)}. {rtt}")
                        return await ctx.reply(file=gfile, embed=inbed)
                except Exception:
                    return await ctx.send(f'something went wrong mate')

    @commands.command()
    async def gen(
            self,
            ctx,
            *,
            prompt: str = commands.parameter(description="The prompt to use for generation")
    ):
        """Generate an image from a privately hosted stable diffusion API.

        examples:
            !gen puppy
            !gen tall drink of water

            This command only takes a prompt, no additonal options. no quotes required.
            uses default options of 30 steps, cfg 12.5, 512x512px

            to customize options use the generate command instead
        """

        params = {
            "prompt": prompt,
            "width": 512,
            "height": 512,
            "steps": 30,
            "cfg_scale": 12.5,
            "sampler_index": "Euler a"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.config['generate']['api_url']}/sdapi/v1/txt2img", json=params,
                                    timeout=-1) as resp:
                if resp.status != 200:
                    await self.error_embed(ctx, 'API error', f'the response status was not ok. response: {resp.status}')

                data = await resp.json()
                try:
                    for i in data['images']:
                        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
                        image.save('img.png')
                        inbed = discord.Embed(title="Generated image", description=prompt, color=0xBA55D3)
                        gfile = discord.File("img.png", filename="img.png")
                        inbed.set_image(url='attachment://img.png')
                        await ctx.reply(file=gfile, embed=inbed)
                except Exception:
                    await ctx.send(f'something went wrong mate')

    @commands.command()
    async def genstatus(self, ctx):
        """the status of the stable diffusion API.

        now with 100% more progress bars!

        if the queue is empty this will just silently delete your command
        """

        embedsent = False
        async with aiohttp.ClientSession() as session:
            gif = random.choice(status_gifs)
            gifpath = f"assets/{gif}"
            while True:
                async with session.get(
                        f"{self.config['generate']['api_url']}/sdapi/v1/progress?skip_current_image=false") as resp:
                    if resp.status != 200:
                        await self.error_embed(ctx, 'API error',
                                               f'the response status was not ok. response: {resp.status}')

                    data = await resp.json()
                    if int(data['state']['job_count']) > 0:
                        nicetext = f"{self.progress_bar(data['state']['sampling_step'], data['state']['sampling_steps'])}\nETA: {self.pretty_time_delta(data['eta_relative'])}\nstep: {data['state']['sampling_step']} of {data['state']['sampling_steps']} "
                        sbed = discord.Embed(title="status", description=nicetext, color=0x2E8B57)
                        sbed.set_image(url=f'attachment://{gif}')
                        if not embedsent:
                            try:
                                afile = discord.File(gifpath, filename=gif)
                                statusembed = await ctx.reply(file=afile, embed=sbed)
                                embedsent = True
                            except Exception:
                                return await ctx.send(f'something went wrong mate')
                        else:
                            await statusembed.edit(embed=sbed)
                    elif embedsent:
                        await statusembed.delete()
                        catcall = ctx.message
                        return await catcall.delete()
                    else:
                        catcall = ctx.message
                        return await catcall.delete()
                    await asyncio.sleep(10)

    @staticmethod
    def pretty_time_delta(seconds):
        seconds = int(seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return f'{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds'
        elif hours > 0:
            return f'{hours} hours, {minutes} minutes, and {seconds} seconds'
        elif minutes > 0:
            return f'{minutes} minutes, and {seconds} seconds'
        else:
            return f'{seconds} seconds'

    @staticmethod
    def progress_bar(progress, total):
        # calculate the fraction
        fraction = progress / total
        # calculate the percentage
        percentage = fraction * 100
        # calculate the length of the progress bar
        length = 40
        # calculate the number of # characters
        num_hash = int(round(length * fraction))
        # build the progress bar string
        progress_bar_str = '[' + '#' * num_hash + '\_' * (length - num_hash) + ']' + ' ' + str(int(percentage)) + '%'
        # return the progress bar string
        return progress_bar_str

    @staticmethod
    def error_embed(ctx, error='', details=''):
        embed = discord.Embed(title=error, description=details, color=discord.Colour.red())
        errorfile = discord.File("assets/gpu_error.png", filename="gpu_error.png")
        embed.set_thumbnail(url='attachment://gpu_error.png')
        return ctx.send(file=errorfile, embed=embed)


async def setup(bot):
    await bot.add_cog(GenerateCog(bot))
