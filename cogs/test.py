"""Cog to test out commands and other stuff"""

import discord
from discord.ext import commands

class Test(commands.Cog):
    """For debugging purposes"""

    def __init__(self, bot):
        self.bot = bot
    

    # @commands.command()s
    # async def listlangs(self, context):
    #     """Lists all available languages"""
    #     results = translate_client.get_languages()

    #     await context.send(results)


def setup(bot):
    bot.add_cog(Test(bot))

