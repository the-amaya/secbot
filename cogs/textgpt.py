import discord
from discord.ext import commands, tasks
import sqlite3
from datetime import datetime
import asyncio
import json
import requests
import queue
import aiohttp
import configparser


class TextGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = queue.Queue()
        self.settings_file_name = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_file_name)
        self.HOST = self.config['textgpt']['api_url']
        self.URI = f'http://{self.HOST}/api/v1/chat'

        # Initialize SQLite database
        self.conn = sqlite3.connect('chat.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS gpt (
                               key INTEGER PRIMARY KEY,
                               datetime TEXT,
                               user TEXT,
                               channel TEXT,
                               server TEXT,
                               request TEXT,
                               response TEXT,
                               response_time TEXT )""")
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        self.message_loop.start()
        print('Cog textgpt is ready.')

    @tasks.loop(seconds=1.0)
    async def message_loop(self):
        if not self.queue.empty():
            message_info = self.queue.get()

            key = message_info['key']

            # Show typing action
            async with message_info['context'].channel.typing():
                #print(f"Processing {key}")
                res = await self.chat_gpt(self.URI, message_info['request'])

                # Update response database
                self.cursor.execute("""
                    UPDATE gpt
                    SET response = ?,
                        response_time = ?
                    WHERE key = ?
                """, (res, str(datetime.now()), key))
                self.conn.commit()
                #print(f"Database updated: {key}")

                # Reply to the original message
            res = res.replace("&#x27;", "'")
            res = res.replace("&quot;", "\"")
            res = res.replace("&amp;", "&")
            n = 1950
            if len(res) > n:
                chunks = [res[i:i+n] for i in range(0, len(res), n)]
                count = 1
                for chunk in chunks:
                    sleepcount = count * 5
                    await asyncio.sleep(sleepcount)
                    await message_info['context'].reply(chunk)
                    count = count + 1
            else:
                await message_info['context'].reply(res)

    @commands.command()
    async def gpt(self, ctx, *, content: str):
        """Send your message to a private LLM and receive a response.

        example:
            !gpt how do I plant a tree?

            This command sends everything in your message after the command word to the LLM, no quotes required.

            Please note that the LLM is slow and responses could take some time to generate.
        """
        # Add message to the database
        self.cursor.execute("""
            INSERT INTO gpt(datetime, user, channel, server, request, response, response_time)
            VALUES(?,?,?,?,?,?,?)
        """, (str(datetime.now()), str(ctx.author), str(ctx.channel), str(ctx.guild), content, "", ""))
        self.conn.commit()
        key = self.cursor.lastrowid
        #print(f"Database updated: {key}")

        # Add message to the queue
        self.queue.put({
            'key': key,
            'channel': ctx.channel,
            'request': content,
            'context': ctx
        })

    @staticmethod
    async def chat_gpt(url, message: str) -> str:
        #print("the chatgpt function has been called")
        history = {'internal': [], 'visible': []}
        request = {
            'user_input': message,
            'max_new_tokens': 2048,
            'auto_max_new_tokens': True,
            'history': history,
            'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'Assistant',
            'instruction_template': 'viv-everything',  # Will get autodetected if unset
            # 'context_instruct': '',  # Optional
            'your_name': 'You',

            'regenerate': False,
            '_continue': False,
            'stop_at_newline': False,
            'chat_generation_attempts': 1,
            'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            'preset': 'Divine Intellect',
            'do_sample': True,
            'temperature': 0.7,
            'top_p': 0.1,
            'typical_p': 1,
            'epsilon_cutoff': 0,  # In units of 1e-4
            'eta_cutoff': 0,  # In units of 1e-4
            'tfs': 1,
            'top_a': 0,
            'repetition_penalty': 1.18,
            'repetition_penalty_range': 0,
            'top_k': 40,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,

            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 8192,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': []
        }

        async with aiohttp.ClientSession() as session:
            #print(url)
            async with session.post(url, json=request, timeout=-1) as resp:
                if resp.status != 200:
                    return "Unexpected error, try again later."

                result = await resp.json()
                result = result['results'][0]['history']
                return(result['visible'][-1][1])


async def setup(bot):
    await bot.add_cog(TextGPT(bot))
