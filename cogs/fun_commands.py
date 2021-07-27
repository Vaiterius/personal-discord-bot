"""Cog for fun commands"""
import math
import json
import random
import requests

import discord
from discord.ext import commands
from discord import Message, Member

class FunCommands(commands.Cog, name="Fun"):
    """Command category for fun commands"""
    
    def __init__(self, bot):
        self.bot = bot

        with open("monty_python_quotes.json", encoding="utf-8") as file:
            self.mp_quotes = json.load(file)
    

    @commands.command(name='hello')
    async def _hello(self, context):
        """Says hello back to you"""
        await context.send(f"Hello, {context.author.mention}!")
    

    @commands.command(name='montypython', aliases=['mp'])
    async def _montypython(self, context):
        """Says a random Monty Python quote"""
        await context.send(random.choice(self.mp_quotes))


    @commands.command(name='echo')
    async def _echo(self, context, *, whatever):
        """Echoes whatever you say after the command"""
        await context.send(whatever)


    @commands.command(name='evaluate', aliases=['eval'])
    async def _evaluate(self, context, *, expression):
        """
        Evaluates a mathematical expression for you
        e.g. `gooby eval sin(pi) * 180 + 4`
        """

        # Only allow mathematical functions from the math library.
        ALLOWED_NAMES = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }

        # Compile the expression.
        code = compile(expression, "<string>", "eval")

        # Validate allowed names.
        for name in code.co_names:
            if name not in ALLOWED_NAMES:
                raise NameError(f"The use of '{name}' is not allowed")

        await context.send(eval(code, {"__builtins__": {}}, ALLOWED_NAMES))


    @commands.command(name="8ball")
    async def _8ball(self, context, *, question):
        """Ask the wise 8ball and it will respond!"""
        affirmatives = (
            "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.",
            "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.")
        non_committals = (
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.")
        negatives = (
            "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful.")
        
        pick = random.uniform(0, 1)

        # 50% chance to pick an affirmative answer.
        if pick <= 0.5:
            await context.send(random.choice(affirmatives))
        # 25% chance to pick an unsure answer.
        elif pick <= 0.75:
            await context.send(random.choice(non_committals))
        # 25% chance to pick a negative answer.
        else:
            await context.send(random.choice(negatives))
    

    @commands.command(name='clone', aliases=['cl'])
    async def _clone(self, context, mention: Member, *, message):
        """Clones whoever you mention and fake a message!"""
        nickname = mention.nick
        if not mention.nick:
            nickname = mention.name

        webhook = await context.channel.create_webhook(
            name=nickname)

        # Delete the message you just made.
        await Message.delete(context.message)

        # Send a fake message from someone you impersonated.
        await webhook.send(
            content=message,
            username=nickname,
            avatar_url=mention.avatar_url)
        
        await webhook.delete()
    

    @commands.command(name='xkcd')
    async def _xkcd(self, context, pick):
        """
        Gets the current xkcd comic or fetches a random one
        e.g. `gooby xkcd random` or `gooby xkcd current`"""

        curr_num = json.loads(requests.get("https://xkcd.com/info.0.json").text)["num"]

        comic = None
        if pick.lower() == "current":
            comic = json.loads(requests.get(f"https://xkcd.com/{curr_num}/info.0.json").text)
        elif pick.lower() == "random":
            rand_num = random.randint(1, curr_num)
            comic = json.loads(requests.get(f"https://xkcd.com/{rand_num}/info.0.json").text)
        
        embed = discord.Embed(title=comic["title"], color=discord.Color.blurple())
        embed.add_field(name="Date", value=f"{comic['month']}/{comic['day']}/{comic['year']}", inline=False)
        embed.add_field(name=f"No.", value=comic['num'], inline=False)
        if comic['news']:
            embed.add_field(name="News", value=comic['news'], inline=False)
        # if comic['transcript']:
        #     embed.add_field(name="Transcript", value=comic['transcript'], inline=False)
        embed.add_field(name=f"Alternate text", value=comic['alt'], inline=False)
        embed.set_image(url=comic["img"])

        await context.send(embed=embed)
    

    @commands.command(name='roll')
    async def _roll(self, context, sides: int):
        """Roll a dice with selected number of sides"""
        sides = int(sides)
        await context.send(random.randint(1, sides))
    

    @commands.command(name='coinflip', aliases=['cf', 'flip'])
    async def _coinflip(self, context):
        """Heads or tails?"""
        side = random.randint(1, 2)
        if side == 1:
            await context.send("Heads!")
        else:
            await context.send("Tails!")


def setup(bot):
    bot.add_cog(FunCommands(bot))

