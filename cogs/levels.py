import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog
from tools import DB

class LevelsSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_data(self, member):
        DB.update_member(member = DB.Member(UserID=member["user_id"],
                                            GuildID=member["guild_id"],
                                            currentExp=member["current_exp"],
                                            currentLevel=member["current_level"]))

    async def add_exp(self, members, exp):
        members['current_exp'] += exp

    async def level_up(self, message: discord.Message, members, channel):
        experience = members['current_exp']
        lvl_start = members['current_level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            await channel.send('{} has leveled up to level {}'.format(message.author.mention, lvl_end))
            members['current_level'] = lvl_end

    @Cog.listener()
    async def on_member_join(self, member):
        DB.insert_member(member = DB.Member(UserID=member["user_id"],
                                            GuildID=member["guild_id"],
                                            currentExp=0,
                                            currentLevel=0))

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        member = DB.get_member(message.author.id, message.guild.id)

        await self.add_exp(member, random.randint(1, 15))
        await self.level_up(message, member, message.channel)
        await self.update_data(member)


async def setup(bot):
    await bot.add_cog(LevelsSystem(bot))