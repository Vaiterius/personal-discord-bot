"""Cog for general commands"""
import discord
from discord.ext import commands

class GeneralCommands(commands.Cog, name="General"):
    """Command category for generic commands"""
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        description="Displays (of server) name, ID, region, size, owner, channels, and roles.")
    async def serverinfo(self, context):
        """Displays server information"""
        name = context.guild.name
        id = context.guild.id
        region = context.guild.region
        size = context.guild.member_count
        owner = context.guild.owner
        voice_channels = "\n".join(str(channel) for channel in context.guild.voice_channels)
        text_channels = "\n".join(str(channel) for channel in context.guild.text_channels)
        roles = "\n".join(str(role) for role in context.guild.roles)

        # Format information in a neat, embedded way.
        embed = discord.Embed(title="Server Information", description=name)

        embed.add_field(name="Owner", value=owner, inline=False)
        embed.add_field(name="Server ID", value=id, inline=False)
        embed.add_field(name="Region", value=region, inline=False)
        embed.add_field(name="Member count", value=size, inline=False)
        embed.add_field(name="Roles", value=roles, inline=False)
        embed.add_field(name="Text channels", value=text_channels, inline=True)
        embed.add_field(name="Voice channels", value=voice_channels, inline=True)

        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))

