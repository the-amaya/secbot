import asyncio
import discord
import sqlite3
import re

from discord.ext import commands

# TODO test


class CustomReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('custom_reactions.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS custom_reactions(server_id INTEGER, trigger_word TEXT, "
                            "reaction_message TEXT)")

    @commands.Cog.listener()
    async def on_message(self, message):
        # make sure the bot doesn't react to itself
        if message.author.id == self.bot.user.id:
            return

        # loop through the custom reactions for the server
        self.cursor.execute("SELECT * FROM custom_reactions WHERE server_id = ?", (message.guild.id,))
        reactions = self.cursor.fetchall()

        for reaction in reactions:
            # check if the message contains the trigger word
            if re.search(reaction[1], message.content, re.IGNORECASE):
                # send the reaction message
                await message.channel.send(reaction[2])

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_reaction(self, ctx, trigger_word: str, reaction_message: str):
        """
        Add a new custom reaction for this server.
        When someone says the $trigger_word the bot will respond with the $reaction_message
        """
        # add the new custom reaction
        self.cursor.execute("INSERT INTO custom_reactions VALUES (?, ?, ?)",
                            (ctx.guild.id, trigger_word, reaction_message))
        self.db.commit()
        await ctx.send("Custom reaction added successfully!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_reaction(self, ctx, trigger_word: str):
        """
        delete a custom reaction for this server.
        delete the custom reaction for this server with the trigger word provided.
        dont know what you want to delete? look it up with list_reactions
        """
        # remove the custom reaction
        self.cursor.execute("DELETE FROM custom_reactions WHERE server_id = ? and trigger_word = ?",
                            (ctx.guild.id, trigger_word))
        self.db.commit()
        await ctx.send("Custom reaction removed successfully!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_reactions(self, ctx):
        """
        list all the custom reactions configured for the current server
        """
        # get a list of all custom reactions
        self.cursor.execute("SELECT * FROM custom_reactions WHERE server_id = ?", (ctx.guild.id,))
        reactions = self.cursor.fetchall()

        if not reactions:
            await ctx.send("No custom reactions found!")
            return

        # build a list of the reactions
        message = "**Custom Reactions:**\n"
        for reaction in reactions:
            message += f"`{reaction[1]}`: {reaction[2]}\n"

        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(CustomReactions(bot))
