"""Gooby bot for discord"""
import os
import random
from itertools import cycle

import discord
from discord.channel import TextChannel
from discord.ext import commands, tasks

TOKEN = os.environ["DISCORD_TOKEN"]

description = "Da Gooby Bot\nUse the prefix 'gooby ' (or 'gby ' or 'gb ') before every command!\ne.g. `gooby hello`\n\nSend me more ideas for this bot!"


# class CustomHelpCommand(commands.HelpCommand):d

#     def __init__(self):
#         super().__init__()

    
#     async def send_bot_help(self, mapping):
#         for cog in mapping:
#             print(cog)
#             await self.get_destination().send(
#                 f"{cog.qualified_name}: {[command.name for command in mapping[cog]]}")


#     async def send_cog_help(self, cog):
#         await self.get_destination().send(
#             f"{cog.qualified_name}: {[command.name for command in cog.get_commands()]}"
#         )


#     async def send_group_help(self, group):
#         await self.get_destination().send(
#             f"{group.name}: {[command.name for index, command in enumerate(group.commands)]}"
#         )


#     async def send_command_help(self, command):
#         await self.get_destination().send(command.name)


intents = discord.Intents(
    members=True,
    messages=True,
    guilds=True,
    webhooks=True,
    voice_states=True,
    emojis=True,
    guild_messages=True,
    guild_reactions=True)

bot = commands.Bot(
    command_prefix=['gooby ', 'gby ', 'gb '],
    case_insensitive=True,  # For commands, not the prefix.
    description=description,
    intents=intents,
    help_command=commands.MinimalHelpCommand())
# bot.remove_command("help")  # We want to place it under the General category.

# Me and my alt account.
owner_ids = (354783154126716938, 691896247052927006)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(f"Discord.py version: {discord.__version__}")
    print("--------")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Streaming(name="Don't click my stream",
                                   url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    # change_status.start()


# status = cycle(["Status 1", "Status 2", "Status 3"])
# @tasks.loop(seconds=30)
# async def change_status():
#     await bot.change_presence(activity=discord.Game(next(status)))


@bot.command()
@commands.has_permissions(administrator=True)
async def load(context, extension):
    """(Bot dev only) Load a cog into the bot"""
    if context.author.id in owner_ids:
        bot.load_extension(f"cogs.{extension}")
        print(f"File load of {extension}.py successful.")
        await context.send(f"File load of {extension}.py successful.")
    else:
        await context.send("You do not have permission to do this")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(context, extension):
    """(Bot dev only) Unload a cog from the bot"""
    if context.author.id in owner_ids:
        bot.unload_extension(f"cogs.{extension}")
        print(f"File unload of {extension}.py successful.")
        await context.send(f"File unload of {extension}.py successful.")
    else:
        await context.send("You do not have permission to do this")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(context, extension):
    """(Bot dev only) Reload a cog into the bot"""
    if context.author.id in owner_ids:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        print(f"File reload of {extension}.py successful.")
        await context.send(f"File reload of {extension}.py successful.")
    else:
        await context.send("You do not have permission to do this")


# Load cogs into the bot.
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(TOKEN)
