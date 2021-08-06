"""Cog for bot listener events and interactions"""
import random

from discord.ext import commands


class ChatListener(commands.Cog):
    """Listens to non-command events in the chat"""

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        """Interact with the chat with greetings and other messages"""
        username = str(message.author.name)
        user_message = str(message.content)
        split_message = user_message.lower().split()
        channel = str(message.channel.name)

        # Don't respond to own messages.
        if message.author == self.bot.user:
            return

        # Positive greetings from user.
        greetings = (
            'hey', 'hi', 'hello', 'sup', 'howdy', 'hola', 'yo', 'hallo', 'bonjour', 'privyet',
            'gm', 'good morning', 'good afternoon', 'welcome', 'good day', 'gday', "g'day",
            'buenos dias', 'buenas tardes', 'shalom', 'sup', "what's up", 'wassup', 'wassap')
        pos_responses = (
            "Why hello there!", "Greetings!", "Hey, how are ya?", "Hello!", )
        
        # Negative greetings from user.
        insults = (
            "fuck you", "fuck off", "go fuck yourself", "you a little bitch", "you a lil bitch",
            "suck my dick", "kiss my ass", "suck my nuts", "eat my ass", "fuck", "piss off")
        neg_responses = (
            "Come back when you've learned some manners", "I am not amused", "That was very naughty",
            "You kiss your mother with that mouth?", "Take a chill pill bro", "Watch yo profanity")
        
        try:
            if split_message[0] in greetings and split_message[1].startswith("gooby"):
                await message.channel.send(random.choice(pos_responses))
            elif user_message.startswith(insults) and "gooby" in split_message:
                await message.channel.send(random.choice(neg_responses))
        except IndexError as e:
            pass
        except Exception as e:
            print(f"FROM LISTENER COG: {e}")


async def setup(bot):
    await bot.add_cog(ChatListener(bot))

