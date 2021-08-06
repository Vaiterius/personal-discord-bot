<<<<<<< HEAD:cogs/troll.py
"""Cog just for trolls and laughs"""
import os
import random
from asyncio import sleep
from datetime import datetime

import pymongo
import audioread
import discord
from discord.ext import commands

mongo_url = os.environ["MONGO_GOOBY_URL"]

class Troll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Setup MongoDB authentication and fetch GoobyDB.guild info collection.
        self.cluster = pymongo.MongoClient(mongo_url)
        self.db = self.cluster["GoobyDB"]
        self.collection = self.db["guild_troll_db"]

        # Me and my alt account. main: 354783154126716938, alt: 691896247052927006
        self.owner_ids = [354783154126716938, 691896247052927006]
    

    def _guild_in_database(self, guild) -> bool:
        """Return True or False whether the guild is found inside the database"""
        in_db = self.collection.count_documents({"guild_id": guild.id}) != 0
        return in_db

    
    def _create_guild_database(self, guild) -> None:
        """Takes in the guild object and creates a new spot for it in the database"""
        # Guild document base template.
        guild_info = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "troll_toggle_status": {
                "chat_listener": False,
                "vc_listener": False,
            },
            "last_to_toggle": {
                "name": "None",
                "action": "None",
                "time": "None",
            },
        }
        # Upload it into the database.
        self.collection.insert_one(guild_info)
    

    def _check_if_admin_or_dev(self, author) -> bool:
        """Return True if a troll command is invoked by a bot dev or a server admin"""
        if author.id in self.owner_ids:
            return True
        elif author.guild_permissions.administrator is True:
            return True
        return False


    ##################################
    ##### CHAT LISTENER FUNCTION #####
    ##################################

    @commands.Cog.listener()
    async def on_message(self, message):
        """Idek man"""
        # So that the bot doesn't infinitely respond to itself.
        if message.author == self.bot.user:
            return

        # Create a new database document for the guild if not already there.
        if not self._guild_in_database(message.guild):
            self._create_guild_database(message.guild)
        
        try:
            # Return if the chat listener is toggled False.
            tt_chat = self.collection.find_one({"guild_id": message.guild.id})["troll_toggle_status"]["chat_listener"]
            if tt_chat is False:
                return
        except Exception as e:
            # Return if the database couldn't be accessed.
            print(f"ERROR from chat listener: {e}")
            return

        username = str(message.author.name)
        user_message = str(message.content)
        split_message = user_message.lower().split()
        channel = str(message.channel.name)
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

    ########################################
    ##### VOICE CHAT LISTENER FUNCTION #####
    ########################################

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Whenever a user joins, the bot joins and plays an randomly-selected audio file"""

        # Create a new database document for the guild if not already there.
        if not self._guild_in_database(member.guild):
            self._create_guild_database(member.guild)
        
        try:
            # Return if the chat listener is toggled False.
            tt_vc = self.collection.find_one({"guild_id": member.guild.id})["troll_toggle_status"]["vc_listener"]
            if tt_vc is False:
                return
        except Exception as e:
            # Return if the database couldn't be accessed.
            print(f"ERROR from VC listener: {e}")
            return

        audio_files = [audio for audio in os.listdir("./audio_files")]

        vc_before = before.channel
        vc_after = after.channel
        
        if vc_before == vc_after:
            return
        if vc_before is None:
            try:
                source_file = f"audio_files/{random.choice(audio_files)}"
                channel = member.voice.channel
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(source_file))
                with audioread.audio_open(source_file) as f:
                    await sleep(f.duration)
                await vc.disconnect()
            except Exception as e:
                print(f"EXCEPTION FROM VC: {e}")

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

    ###################################
    ##### TROLL TOGGLING FUNCTION #####
    ###################################

    @commands.command(name='toggletroll', aliases=['tt', 'toggle'])
    async def _toggle_troll(self, context, code):
        """
        Toggle options if you don't want these features

        **NOTE** These toggles are True (on) by default whenever the bot restarts
        of if this Cog is reloaded/loaded.

        **CODE**
        s - show troll toggle status
        0 - disable troll chat listener
        1 - disable troll vc listener

        e.g. `gby tt s`
        """
        # Ignore bots.
        if context.author == self.bot.user:
            return
        if context.author.bot:
            return

        # Create a new database document for the guild if not already there.
        if not self._guild_in_database(context.guild):
            self._create_guild_database(context.guild)

        author = context.author
        author_id = context.author.id
        guild_name = context.guild.name
        guild_id = context.guild.id

        # Our boolean values.
        tt_chat_listener = self.collection.find_one({"guild_id": context.guild.id})["troll_toggle_status"]["chat_listener"]
        tt_vc_listener = self.collection.find_one({"guild_id": context.guild.id})["troll_toggle_status"]["vc_listener"]

        try:
            code = int(code)
        except ValueError:  # If code is a string instead.
            # Send the status toggles to the channel where command was invoked.
            if code in ['s', "status", "statuses"]:
                try:
                    name = self.collection.find_one({"guild_id": context.guild.id})["last_to_toggle"]["name"]
                    action = self.collection.find_one({"guild_id": context.guild.id})["last_to_toggle"]["action"]
                    time = self.collection.find_one({"guild_id": context.guild.id})["last_to_toggle"]["time"]
                    
                    # Make an embedded toggle status format.
                    embed = discord.Embed(title="__Troll Toggle Status__", color=discord.Color.blurple())
                    embed.add_field(name=f"[0] Chat Listener", value=f"`{tt_chat_listener}`", inline=True)
                    embed.add_field(name=f"[1] VC Listener", value=f"`{tt_vc_listener}`", inline=True)
                    embed.add_field(
                        name="Last toggled",
                        value=f"_Action:_ `{action}`\n_by:_ `{name}`\n_@:_ `{time}`",
                        inline=False)
                except Exception as e:
                    print(f"EXCEPTION FROM TTS: {e}")

                print(f"Troll toggle status invoked by {context.author.name}")
                await context.send(embed=embed)
        else:
            # If code is an integer instead.
            # Toggle each listener depending on code chosen.

            ### CHAT LISTENER ###
            if code == 0:
                # Only the admins or a bot developer may use this troll command.
                if not self._check_if_admin_or_dev(author):
                    await context.send("You do not have permissions for this command!")
                    return

                time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                update_tt_chat_listener = not tt_chat_listener
                # Update database.
                self.collection.update({"guild_id": guild_id}, {
                    "$set": {
                        "troll_toggle_status": {
                            "chat_listener": update_tt_chat_listener,  # Invert the value to toggle.
                            "vc_listener": tt_vc_listener,
                        },
                        "last_to_toggle": {
                            "name": str(author),
                            "action": "Toggled troll chat listener",
                            "time": time,
                        },
                    }
                })

                print(f"Chat listener toggled: `{update_tt_chat_listener}`")
                await context.send(f"Chat listener toggled: `{update_tt_chat_listener}`")

            ### VC LISTENER ###
            elif code == 1:
                # Only the admins or a bot developer may use this troll command.
                if not self._check_if_admin_or_dev(author):
                    await context.send("You do not have permissions for this command!")
                    return

                time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                update_tt_vc_listener = not tt_vc_listener
                # Update database.
                self.collection.update({"guild_id": guild_id}, {
                    "$set": {
                        "troll_toggle_status": {
                            "chat_listener": tt_chat_listener,
                            "vc_listener": update_tt_vc_listener,  # Invert the value to toggle.
                        },
                        "last_to_toggle": {
                            "name": str(author),
                            "action": "Toggled troll VC listener",
                            "time": time,
                        },
                    }
                })

                print(f"VC listener toggled: `{update_tt_vc_listener}`")
                await context.send(f"VC listener toggled: `{update_tt_vc_listener}`")


def setup(bot):
    bot.add_cog(Troll(bot))

=======
"""Cog just for trolls and laughs"""
import os
import random
from asyncio import sleep
from datetime import datetime

import pymongo
import audioread
import discord
from discord.ext import commands

mongo_url = os.environ.get("MONGO_GOOBI_URL")

class Troll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Setup MongoDB authentication and fetch GoobyDB.guild info collection.
        self.cluster = pymongo.MongoClient(mongo_url)
        self.db = self.cluster["GoobyDB"]
        self.collection = self.db["guild_troll_db"]

        # Me and my alt account. main: 354783154126716938, alt: 691896247052927006
        self.owner_ids = [354783154126716938, 691896247052927006]
    

    def _guild_in_database(self, guild) -> bool:
        """Return True or False whether the guild is found inside the database"""
        in_db = self.collection.count_documents({"guild_id": guild.id}) != 0
        return in_db

    
    def _create_guild_database(self, guild) -> None:
        """Takes in the guild object and creates a new spot for it in the database"""
        # Guild document base template.
        guild_info = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "troll_toggle_status": {
                "chat_listener": False,
                "vc_listener": False,
            },
            "last_to_toggle": {
                "name": "None",
                "action": "None",
                "time": "None",
            },
        }
        # Upload it into the database.
        self.collection.insert_one(guild_info)
    

    def _check_if_admin_or_dev(self, author) -> bool:
        """Return True if a troll command is invoked by a bot dev or a server admin"""
        if author.id in self.owner_ids:
            return True
        elif author.guild_permissions.administrator is True:
            return True
        return False


    ##################################
    ##### CHAT LISTENER FUNCTION #####
    ##################################

    @commands.Cog.listener()
    async def on_message(self, message):
        """Idek man"""
        # So that the bot doesn't infinitely respond to itself.
        if message.author == self.bot.user:
            return

        # Create a new database document for the guild if not already there.
        if not self._guild_in_database(message.guild):
            self._create_guild_database(message.guild)
        
        try:
            # Return if the chat listener is toggled False.
            tt_chat = self.collection.find_one({"guild_id": message.guild.id})["troll_toggle_status"]["chat_listener"]
            if tt_chat is False:
                return
        except Exception as e:
            # Return if the database couldn't be accessed.
            print(f"ERROR from chat listener: {e}")
            return

        username = str(message.author.name)
        user_message = str(message.content)
        split_message = user_message.lower().split()
        channel = str(message.channel.name)
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

    ########################################
    ##### VOICE CHAT LISTENER FUNCTION #####
    ########################################

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Whenever a user joins, the bot joins and plays an randomly-selected audio file"""

        # Create a new database document for the guild if not already there.
        if not self._guild_in_database(member.guild):
            self._create_guild_database(member.guild)
        
        try:
            # Return if the chat listener is toggled False.
            tt_vc = self.collection.find_one({"guild_id": member.guild.id})["troll_toggle_status"]["vc_listener"]
            if tt_vc is False:
                return
        except Exception as e:
            # Return if the database couldn't be accessed.
            print(f"ERROR from VC listener: {e}")
            return

        audio_files = [audio for audio in os.listdir("./audio_files")]

        vc_before = before.channel
        vc_after = after.channel
        
        if vc_before == vc_after:
            return
        if vc_before is None:
            try:
                source_file = f"audio_files/{random.choice(audio_files)}"
                channel = member.voice.channel
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(source_file))
                with audioread.audio_open(source_file) as f:
                    await sleep(f.duration)
                await vc.disconnect()
            except Exception as e:
                print(f"EXCEPTION FROM VC: {e}")

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

    ###################################
    ##### TROLL TOGGLING FUNCTION #####
    ###################################

    @commands.command(name='toggletroll', aliases=['tt', 'toggle'])
    async def _toggle_troll(self, context, code):
        """
        Toggle options if you don't want these features

        **NOTE** These toggles are True (on) by default whenever the bot restarts
        of if this Cog is reloaded/loaded.

        **CODE**
        s - show troll toggle status
        0 - disable troll chat listener
        1 - disable troll vc listener

        e.g. `gby tt s`
        """
        # Ignore bots.
        if context.author == self.bot.user:
            return
        if context.author.bot:
            return

        # Create a new database document for the guild if not already there.
        if not self._guild_in_database(context.guild):
            self._create_guild_database(context.guild)

        author = context.author
        author_id = context.author.id
        guild_name = context.guild.name
        guild_id = context.guild.id

        # Our boolean values.
        tt_chat_listener = self.collection.find_one({"guild_id": context.guild.id})["troll_toggle_status"]["chat_listener"]
        tt_vc_listener = self.collection.find_one({"guild_id": context.guild.id})["troll_toggle_status"]["vc_listener"]

        try:
            code = int(code)
        except ValueError:  # If code is a string instead.
            # Send the status toggles to the channel where command was invoked.
            if code in ['s', "status", "statuses"]:
                try:
                    name = self.collection.find_one({"guild_id": context.guild.id})["last_to_toggle"]["name"]
                    action = self.collection.find_one({"guild_id": context.guild.id})["last_to_toggle"]["action"]
                    time = self.collection.find_one({"guild_id": context.guild.id})["last_to_toggle"]["time"]
                    
                    # Make an embedded toggle status format.
                    embed = discord.Embed(title="__Troll Toggle Status__", color=discord.Color.blurple())
                    embed.add_field(name=f"[0] Chat Listener", value=f"`{tt_chat_listener}`", inline=True)
                    embed.add_field(name=f"[1] VC Listener", value=f"`{tt_vc_listener}`", inline=True)
                    embed.add_field(
                        name="Last toggled",
                        value=f"_Action:_ `{action}`\n_by:_ `{name}`\n_@:_ `{time}`",
                        inline=False)
                except Exception as e:
                    print(f"EXCEPTION FROM TTS: {e}")

                print(f"Troll toggle status invoked by {context.author.name}")
                await context.send(embed=embed)
        else:
            # If code is an integer instead.
            # Toggle each listener depending on code chosen.

            ### CHAT LISTENER ###
            if code == 0:
                # Only the admins or a bot developer may use this troll command.
                if not self._check_if_admin_or_dev(author):
                    await context.send("You do not have permissions for this command!")
                    return

                time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                update_tt_chat_listener = not tt_chat_listener
                # Update database.
                self.collection.update({"guild_id": guild_id}, {
                    "$set": {
                        "troll_toggle_status": {
                            "chat_listener": update_tt_chat_listener,  # Invert the value to toggle.
                            "vc_listener": tt_vc_listener,
                        },
                        "last_to_toggle": {
                            "name": str(author),
                            "action": "Toggled troll chat listener",
                            "time": time,
                        },
                    }
                })

                print(f"Chat listener toggled: `{update_tt_chat_listener}`")
                await context.send(f"Chat listener toggled: `{update_tt_chat_listener}`")

            ### VC LISTENER ###
            elif code == 1:
                # Only the admins or a bot developer may use this troll command.
                if not self._check_if_admin_or_dev(author):
                    await context.send("You do not have permissions for this command!")
                    return

                time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                update_tt_vc_listener = not tt_vc_listener
                # Update database.
                self.collection.update({"guild_id": guild_id}, {
                    "$set": {
                        "troll_toggle_status": {
                            "chat_listener": tt_chat_listener,
                            "vc_listener": update_tt_vc_listener,  # Invert the value to toggle.
                        },
                        "last_to_toggle": {
                            "name": str(author),
                            "action": "Toggled troll VC listener",
                            "time": time,
                        },
                    }
                })

                print(f"VC listener toggled: `{update_tt_vc_listener}`")
                await context.send(f"VC listener toggled: `{update_tt_vc_listener}`")


async def setup(bot):
    await bot.add_cog(Troll(bot))

>>>>>>> ce788bb... Update libraries and do cleanup:bot/cogs/troll.py
