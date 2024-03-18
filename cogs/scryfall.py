import discord
from discord.ext import commands
import requests
import urllib


class ScryfallCog(commands.Cog, name="Scryfall Commands"):
    """
    Scryfall Magic: The Gathering Card Information.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.card_search_url = "https://api.scryfall.com/cards/search"
        self.autocomplete_url = 'https://api.scryfall.com/cards/autocomplete'
        self.random_card_url = 'https://api.scryfall.com/cards/random'
        self.random_commander_url = 'https://api.scryfall.com/cards/random?q=is%3Acommander'

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog scryfall is ready.')

    @staticmethod
    def format_card_response(card_data):
        """Format the card response as a Discord embed."""
        embed = discord.Embed(title=card_data['name'], colour=discord.Colour.blue())
        embed.add_field(name="Mana Cost", value=card_data.get('mana_cost', 'N/A'), inline=True)
        embed.add_field(name="Type", value=card_data.get('type_line', 'N/A'), inline=True)
        embed.add_field(name="scryfall link", value=card_data.get('scryfall_uri'))

        oracle_text = card_data.get('oracle_text', 'N/A')
        if len(oracle_text) > 1024:  # Embed field value limit is 1024
            oracle_text = oracle_text[:1021] + '...'
        embed.add_field(name="Oracle Text", value=oracle_text, inline=False)

        embed.set_image(url=card_data['image_uris']['normal'])

        return embed

    @staticmethod
    def format_search_response(name_list, search_string):
        """Format the search response as a Discord embed."""
        embed = discord.Embed(title=f"search results for '{search_string}'", colour=discord.Colour.blue())
        result_text = name_list
        result_text = "\n".join(result_text)
        if len(result_text) > 1024:  # Embed field value limit is 1024
            result_text = result_text[:1021] + '...'
        embed.add_field(name="results", value=result_text, inline=False)

        return embed
    
    @commands.command()
    async def card_search(
            self,
            ctx,
            *,
            card_name: str = commands.parameter(description="the name of a MTG card to search for.")
    ):
        """Look up Magic: The Gathering card information on Scryfall by name. returns the first result"""
        
        params = card_name
        requrl = self.card_search_url + '?q=' + urllib.parse.quote(params)
        response = requests.get(requrl)

        if response.status_code == 200:
            data = response.json()
            if data.get('object') == 'error' and data.get('code') == 'not_found':
                await ctx.send(f"No results found for '{card_name}'. details: {data.get('details')}")
            elif data.get('object') == 'list' and data.get('total_cards') > 0:
                card_data = data['data'][0]
                await ctx.send(embed=self.format_card_response(card_data))
            else:
                await ctx.send(f"No results found for '{card_name}'.")
        else:
            data = response.json()
            if data.get('object') == 'error' and data.get('code') == 'not_found':
                await ctx.send(f"No results found for '{card_name}'. details: {data.get('details')}")
            else:
                with open('scryfall_error.txt', 'a+') as f:
                    f.write(f"url used {requrl}, response code: {response.status_code}")
                await ctx.send(f"Error fetching data from Scryfall. response code: {response.status_code}")

    @commands.command()
    async def card_name_search(
            self,
            ctx,
            *,
            card_name: str = commands.parameter(description="the start of, or part of, a MTG card name")
    ):
        """Get a list of possible matches using an autocomplete search api on Scryfall"""

        params = card_name
        requrl = self.autocomplete_url + '?q=' + urllib.parse.quote(params)
        response = requests.get(requrl)

        if response.status_code == 200:
            data = response.json()
            if data.get('object') == 'error' and data.get('code') == 'not_found':
                await ctx.send(f"No results found for '{card_name}'. details: {data.get('details')}")
            elif data.get('object') == 'catalog' and data.get('total_values') > 0:
                name_list = data['data']
                await ctx.send(embed=self.format_search_response(name_list, card_name))
            else:
                await ctx.send(f"No results found for '{card_name}'.")
        else:
            data = response.json()
            if data.get('object') == 'error' and data.get('code') == 'not_found':
                await ctx.send(f"No results found for '{card_name}'. details: {data.get('details')}")
            else:
                with open('scryfall_error.txt', 'a+') as f:
                    f.write(f"url used {requrl}, response code: {response.status_code}")
                await ctx.send(f"Error fetching data from Scryfall. response code: {response.status_code}")

    @commands.command()
    async def random_card(self, ctx):
        """Fetch and display a random Magic: The Gathering card. card."""
        response = requests.get(self.random_card_url)

        if response.status_code == 200:
            card_data = response.json()
            await ctx.send(embed=self.format_card_response(card_data))
        else:
            await ctx.send("Error fetching data from Scryfall.")

    @commands.command()
    async def random_commander(self, ctx):
        """Fetches a random Magic: The Gathering commander."""
        response = requests.get(self.random_commander_url)

        if response.status_code == 200:
            card_data = response.json()
            await ctx.send(embed=self.format_card_response(card_data))
        else:
            await ctx.send("Error fetching data from Scryfall.")

    @card_search.error
    @random_card.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the card name.')
        else:
            await ctx.send(error + 'An error occurred while processing the command.')


async def setup(bot):
    await bot.add_cog(ScryfallCog(bot))
