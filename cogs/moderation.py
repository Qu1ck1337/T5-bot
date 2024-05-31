import asyncio
import datetime

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
    @app_commands.describe(member="Участник, кого мьютить")
    @app_commands.describe(time="Время мьюта в минутах")
    @app_commands.describe(reason="Причина мьюта")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, time: int, reason: str = None):
        embed = discord.Embed(title=f"Участник {member.display_name} был замьючен на {time} минут",
                              description=reason)
        await member.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=time))
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(title=f"Участник {member.display_name} был размьючен")
        await member.timeout(None)
        await interaction.response.send_message(embed=embed)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("У вас нет прав, чтобы кикать участников сервера!")

    @app_commands.command()
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'Участник {member} был забанен')

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message("У вас нет прав, чтобы банить участников сервера!")

    @app_commands.command()
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        await interaction.guild.unban(user=user, reason=reason)
        await interaction.response.send_message(f"Пользователь {user.display_name} был разбанен на сервере!")

    @app_commands.command()
    async def clear(self, interaction: discord.Interaction, amount: int):
        def check(x):
            print(x.interaction)
            return False

        await interaction.response.defer()
        await interaction.channel.purge(limit=amount + 1, check=lambda x: not x.interaction or x.interaction.id != interaction.id)
        message = await interaction.edit_original_response(content=f'Удалено {amount} сообщений!')
        await message.delete(delay=10)


async def setup(bot):
    await bot.add_cog(Moderation(bot))