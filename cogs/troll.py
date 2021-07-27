"""Cog just for trolls and laughs"""
import os
import random
from asyncio import sleep

import audioread
import discord
from discord.ext import commands

class Troll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.toggle_troll_vc_listener = True
        self.toggle_troll_chat_listener = True
        self.toggle_troll_commands = True
    

    @commands.Cog.listener()
    async def on_message(self, message):
        """Idek man"""

        if not self.toggle_troll_chat_listener:
            return

        username = str(message.author.name)
        user_message = str(message.content)
        split_message = user_message.lower().split()
        channel = str(message.channel.name)

        # So that the bot doesn't infinitely respond to itself.
        if message.author == self.bot.user:
            return

        if 'monke' in user_message.lower() or 'monkey' in user_message.lower():
            await message.channel.send("ooh ooh ah ahh")
        elif 'penis' in user_message.lower():
            await message.channel.send('penis')
        elif 'balls' in user_message.lower():
            await message.channel.send('balls in my face')
        elif 'ur mom' in user_message.lower():
            await message.channel.send('Wow what a comeback :neutral_face:')
        elif 'stfu' in user_message.lower() or "shut up" in user_message.lower() \
            or ('shut the fuck up' in user_message.lower()):
            await message.channel.send(random.choice(['No you, bitch', 'Nah you shut up']))
        elif 'nigga' in user_message.lower() or 'nigger' in user_message.lower():
            await message.channel.send(random.choice(["Whoa whoa whoa watch it", "My nigga do you even have the pass? :neutral_face:"]))
        elif 'ur gay' in user_message.lower():
            await message.channel.send("Lol look who's talking")


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Whenever a user joins, the bot joins and plays an randomly-selected audio file"""

        if not self.toggle_troll_vc_listener:
            return

        audio_files = [audio for audio in os.listdir("./audio_files")]

        vc_before = before.channel
        vc_after = after.channel
        
        if vc_before == vc_after:
            return
        if vc_before is None:
            source_file = f"audio_files/{random.choice(audio_files)}"
            channel = member.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(source_file))
            with audioread.audio_open(source_file) as f:
                await sleep(f.duration)
            await vc.disconnect()

        elif vc_after is None:
            return
        else:
            source_file = f"audio_files/{random.choice(audio_files)}"
            channel = member.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(source_file))
            with audioread.audio_open(source_file) as f:
                await sleep(f.duration)
            await vc.disconnect()
    

    @commands.command(name='toggletroll', aliases=['tt', 'toggle'])
    async def toggle_troll(self, context, code):
        """
        Toggle options if you don't want these features
        __NOTE:__ These toggles are True (on) by default whenever the bot restarts
        of if this Cog is reloaded/loaded.
        **CODE:**
        0 - disable troll chat listener
        1 - disable troll vc listener
        """
        code = int(code)
        if code == 0:
            self.toggle_troll_chat_listener =  not self.toggle_troll_chat_listener
            print("Chat listener toggled:", self.toggle_troll_chat_listener)
            await context.send(f"Chat listener toggled: {self.toggle_troll_chat_listener}")
        elif code == 1:
            self.toggle_troll_vc_listener = not self.toggle_troll_vc_listener
            print("VC listener toggled:", self.toggle_troll_vc_listener)
            await context.send(f"VC listener toggled: {self.toggle_troll_vc_listener}")


def setup(bot):
    bot.add_cog(Troll(bot))


