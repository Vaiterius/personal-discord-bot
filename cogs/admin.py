"""Cog for moderation commands"""
import discord
from discord.ext import commands
from discord import Member

class Admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, commands.MissingPermissions):
            await context.send("You don't have the permissions for that!")
    

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, mention: Member, *, reason=None):
        """
        Allows a mod with Kick Members permission to kick someone out of the server
        May also specify reason if desired (after the mention)
        """
        await mention.kick(reason=reason)
        if reason is None:
            await context.send(f"{mention.mention} just got kicked LOL!")
        else:
            await context.send(f"{mention.mention} has been kicked LOL! Reason: {reason}")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, mention: Member, *, reason=None):
        """
        Allows a mod with Ban Members permission to kick someone out of the server
        May also specify a reason if desired (after the mention)
        """
        await mention.ban(reason=reason)
        if reason is None:
            await context.send(f"{mention.mention} just got banned LMAO!")
        else:
            await context.send(f"{mention.mention} just got banned LMAO! Reason: {reason}")
    

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, context, *, member):
        """
        Allows a mod with Ban Members permission to kick someone out of the server
        e.g. `gooby unban SuperNinja#7705`
        """
        banned_users = await context.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await context.guild.unban(user)
                await context.send(f"Unbanned {user.mention}. Smh.")
                return
    

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, amount: int):
        """
        Clears selected amount of messages above (including yours)
        `e.g. gooby clear 7` would clear 7 messages
        """
        amount = int(amount)
        await context.channel.purge(limit=amount)
        await context.send(f"{amount} messages have been removed.", delete_after=2)


def setup(bot):
    bot.add_cog(Admin(bot))

