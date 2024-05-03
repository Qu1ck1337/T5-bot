import asyncio
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
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'User {member} has been kicked')

    @app_commands.command()
    async def mute(self, interaction: discord.Interaction, member: discord.Member, time: int):
        emb = discord.Embed(title="Участник Был Замучен!")
        await interaction.channel.purge(limit=1)
        await interaction.response.send_message(embed=emb)
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.add_roles(muted_role)
        await asyncio.sleep(time)
        await member.remove_roles(muted_role)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to kick members")

    @app_commands.command()
    @app_commands.default_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'User {member} has been banned')

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to ban members")

    @app_commands.command()
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        await interaction.guild.unban(user=user, reason=reason)

    @app_commands.command()
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f'Удалено {amount} сообщений!', delete_after=2)


async def setup(bot):
    await bot.add_cog(Moderation(bot))