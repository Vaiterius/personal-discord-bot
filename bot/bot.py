"""My personal discord bot"""
import os
import asyncio

import discord
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN")

description = """Goobi Bot\n
                Use the prefix 'goobi ' (shorthands: 'g!', 'gb') before every command!\n
                e.g. `goobi hello`\n\n
                What else should I put in this bot?"""

# My alt account and I.
owner_ids = (354783154126716938, 691896247052927006)

bot = commands.Bot(
    command_prefix=('goobi ', 'gb ', 'g!'),
    owner_ids=owner_ids,
    case_insensitive=True,  # For commands, not the prefix.
    description=description,
    intents=discord.Intents.all(),
    help_command=commands.MinimalHelpCommand())


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


@bot.event
async def on_ready():
    """Do some stuff on bot startup"""
    print('GOOBI BOT INITIATED!')
    print(f"using Discord.py version {discord.__version__}")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Streaming(name="Don't click my stream",
                                   url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))


@bot.command()
async def ping(ctx):
    """Pong back latency"""
    await ctx.send(f"_Pong!_ ({round(bot.latency * 1000, 1)} ms)")


@bot.command()
@commands.has_permissions(administrator=True)
async def load(context, extension):
    """(Bot dev only) Load a cog into the bot"""
    if context.author.id in owner_ids:
        await bot.load_extension(f"cogs.{extension}")
        print(f"File load of {extension}.py successful.")
        await context.send(f"File load of {extension}.py successful.")
    else:
        await context.send("You do not have permission to do this")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(context, extension):
    """(Bot dev only) Unload a cog from the bot"""
    if context.author.id in owner_ids:
        await bot.unload_extension(f"cogs.{extension}")
        print(f"File unload of {extension}.py successful.")
        await context.send(f"File unload of {extension}.py successful.")
    else:
        await context.send("You do not have permission to do this")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(context, extension):
    """(Bot dev only) Reload a cog into the bot"""
    if context.author.id in owner_ids:
        await bot.unload_extension(f"cogs.{extension}")
        await bot.load_extension(f"cogs.{extension}")
        print(f"File reload of {extension}.py successful.")
        await context.send(f"File reload of {extension}.py successful.")
    else:
        await context.send("You do not have permission to do this")


async def load_extensions():
    """Load cogs into the bot"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


asyncio.run(main())
