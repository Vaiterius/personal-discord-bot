"""Cog that allows users to translate text to their target language"""
import os
import six
from math import ceil

import discord
from discord.ext import commands

from google.cloud import translate_v2

class Translator(commands.Cog, name='Translator'):
    """
    Translates text into the target language utilizing
    the OFFICIAL Google Cloud Translation API (Basic
    edition, v2).

    Will transition to either Yandex or Deepl after the
    free 90-day trial (due October 20, 2021) of Google's API
    """
    def __init__(self, bot):
        self.bot = bot
        self.translate_client = translate_v2.Client()
        self.supported_langs = self.translate_client.get_languages()
    

    @commands.command(name='translate', aliases=['t', 'tr', 'tl'])
    async def _translate(self, context, target_lang, *, text, model='nmt'):
        """
        Translate your text into your target language(s)
        e.g. `gooby translate english hola como estas?`
        e.g. `gooby translate russian,japanese,spanish good morning!`
        __NOTE__ multiple target languages require separation by commas with no spaces
        """
        # Handle special characters for translation.
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Handle if multiple target languages were passed.
        langs_passed = target_lang.split(',')
        if len(langs_passed) == 1:  # If only one language was passed.
            # Query and retrieve supported target language and verify.
            fetched_lang = next(
                (language for language in self.supported_langs if (target_lang.title() == language["name"]) or
                (target_lang == language["name"]) or (target_lang.lower() == language['language']) or
                (target_lang == language['language'])), None)

            if fetched_lang is None:
                await context.send(f"'{target_lang}'' is not a supported language!")
                return
            
            # Call the API, embed the message, and send.
            result = self.translate_client.translate(text, target_language=fetched_lang['language'])

            embed = discord.Embed()
            embed.add_field(name='Original text', value=text, inline=True)
            embed.add_field(name=f"{fetched_lang['name']}", value=result['translatedText'], inline=False)

            await context.send(embed=embed)

        elif len(langs_passed) > 1:  # If multiple languages were passed.
            embed = discord.Embed()
            embed.add_field(name='Original text', value=text, inline=True)
            for lang in langs_passed:
                # Query and retrieve supported target languages and verify.
                fetched_lang = next(
                    (language for language in self.supported_langs if (lang.title() == language["name"]) or
                    (lang == language["name"]) or (lang.lower() == language['language']) or
                    (lang == language['language'])), None)
                
                if fetched_lang is None:
                    await context.send(f"'{lang}' is not a supported language, or syntax was incorrect.")
                    continue
                
                # Call the API, embed the message, and send.
                result = self.translate_client.translate(text, target_language=fetched_lang[f"language"])
                embed.add_field(name=f"{fetched_lang['name']}", value=result['translatedText'], inline=False)
            
            await context.send(embed=embed)


    @commands.command(
        name='listlangs', aliases=['ll', 'gl', 'listlanguages', 'getlanguages', 'getlangs'])
    async def _list_languages(self, context, num_pages=7):
        """
        List all supported languages for available translation
        __NOTE__ when translating languages, you may either use their 'code' or it's name,
        e.g. `gooby translate en hola` or `gooby translate english hola` are both fine
        """
        num_pages = num_pages
        lang_list = [f"({lang['language']}) {lang['name']}" for lang in self.supported_langs]
        num_langs = len(lang_list)

        # Populate container with pages of embeds for user to click through.
        pages_dict = {}
        start_slice = 0
        end_slice = ceil(num_langs//num_pages) + 1
        for i in range(num_pages):
            curr_page = f"page_{i+1}"
            curr_page_langs = "\n".join(lang_list[start_slice:end_slice])
            pages_dict[curr_page] = discord.Embed(
                title=f"Supported languages",
                description=f"Page {i+1}/{num_pages}")
            pages_dict[curr_page].add_field(name="Languages", value=curr_page_langs)
            start_slice += ceil(num_langs//num_pages) + 1
            end_slice += ceil(num_langs//num_pages) + 1
        pages = list(pages_dict.items())

        # Add reaction buttons.
        await context.send(f"Total languages supported: {num_langs}")
        message = await context.send(embed=pages[0][1])
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')

        # Only the message author may react to the message.
        def check(reaction, user):
            return (user == context.message.author)
        
        # Handle user reactions to navigate embedded pages.
        i = 0
        reaction = None
        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed=pages[i][1])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed=pages[i][1])
            elif str(reaction) == '▶':
                if i < num_pages - 1:
                    i += 1
                    await message.edit(embed=pages[i][1])
            elif str(reaction) == '⏭':
                i = num_pages - 1
                await message.edit(embed=pages[i][1])
            
            # Wait for reaction to be added and break if timeout.
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                await message.remove_reaction(reaction, user)
            except Exception as e:
                break
        
        # Signify that user can no longer navigate pages due to timeout.
        await message.clear_reactions()
    

    @commands.command(name='detectlang', aliases=['dl', 'detectlanguage'])
    async def _detect_language(self, context, *, text):
        """Detects the text's language"""
        result = self.translate_client.detect_language(text)
        confidence, result_lang = round(result['confidence'] * 100, 3), result['language']
        get_lang = next(
            (language for language in self.supported_langs if result_lang == language['language']), None)
        
        embed = discord.Embed()
        embed.add_field(name='Confidence', value=str(confidence) + '%', inline=True)
        embed.add_field(
            name='Detected Language', value=f"({get_lang['language']}) " + str(get_lang['name']), inline=True)
        embed.add_field(name='Text', value=text, inline=False)

        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Translator(bot))

