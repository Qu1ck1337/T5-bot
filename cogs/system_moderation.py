import time
from collections import Counter

import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Show pingg")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Ping!')


    @app_commands.command()
    @app_commands.default_permissions(kick_members = True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason:str=None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'User {member} has been kicked')

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to kick members")

    @app_commands.command()
    @app_commands.default_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason:str=None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'User {member} has been banned')

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to ban members")

    @app_commands.command()
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        await interaction.guild.unban(user=user, reason=reason)


async def setup(bot):
    await bot.add_cog(Moderation(bot))

