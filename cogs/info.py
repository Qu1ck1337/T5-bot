import time
from collections import Counter

import discord
from discord import app_commands
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Show user's avatar")
    @app_commands.describe(user="User's avatar")
    async def avatar(self, interaction: discord.Interaction,
                     user: discord.User = None):
        embed = discord.Embed(color=discord.Color.yellow())
        embed.set_image(url=user.avatar if user else interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Show information about current server")
    async def server_info(self, interaction: discord.Interaction):
        embed = discord.Embed(title=interaction.guild.name,
                              description=interaction.guild.description,
                              color=discord.Color.yellow())

        members = interaction.guild.members
        people_count = len([member for member in members if not member.bot])
        embed.add_field(name="Members",
                        value=f"All: `{len(members)}`\n"
                              f"People: `{people_count}`\n"
                              f"Bots: `{len(members) - people_count}`")

        channels = interaction.guild.channels

        channel_types = Counter()

        for channel in channels:
            channel_types[channel.type] += 1

        embed.add_field(name="Channels",
                        value=f"All: `{len(channels) - len(interaction.guild.categories)}`\n"
                              f"Text Channels: `{channel_types[discord.ChannelType.text]}`\n"
                              f"Voice Channels: `{channel_types[discord.ChannelType.voice]}`\n"
                              f"{f'Stages: `{channel_types[discord.ChannelType.stage_voice]}`' if channel_types[discord.ChannelType.stage_voice] else ''}\n"
                              f"{f'Forums: `{channel_types[discord.ChannelType.forum]}`' if channel_types[discord.ChannelType.forum] else ''}")

        emojis = interaction.guild.emojis
        animated_emojis_count = len([emoji for emoji in interaction.guild.emojis if emoji.animated])

        embed.add_field(name="Emojis & Stickers",
                        value=f"* **Emojis**\n"
                              f"> All: `{len(emojis)}`\n"
                              f"> Static: `{len(emojis) - animated_emojis_count}`\n"
                              f"> Animated: `{animated_emojis_count}`\n"
                              f"* **Stickers**: `{len(interaction.guild.stickers)}`")

        embed.add_field(name="Verification level",
                        value=f'`{interaction.guild.verification_level.name}`')

        embed.add_field(name="Owner",
                        value=interaction.guild.owner.mention)

        embed.add_field(name="Created at",
                        value=f"<t:{int(time.mktime(interaction.guild.created_at.timetuple()))}:D>")

        if interaction.guild.rules_channel:
            embed.add_field(name="Rules channel",
                            value=interaction.guild.rules_channel.mention)

        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_image(url=interaction.guild.banner)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="Show bot's statistics")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Overall bot's statistics",
                              description=f"Latency: `{int(self.bot.latency * 1000 // 1)}` ms\n"
                                          f"Guilds: `{len(self.bot.guilds)}`\n"
                                          f"Users: `{len(self.bot.users)}`",
                              color=discord.Color.yellow())
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Information(bot))