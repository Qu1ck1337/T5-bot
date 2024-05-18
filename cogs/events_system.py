import discord
from discord.ext import commands
from discord.ext.commands import Cog

from tools import DB


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        DB.insert_guild(guild.id, guild.owner_id)

    @Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        DB.remove_guild(guild.id)


async def setup(bot):
    await bot.add_cog(Events(bot))