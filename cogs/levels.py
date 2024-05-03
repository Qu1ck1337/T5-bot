import json
import random
from discord.ext import commands
from discord.ext.commands import Cog


class LevelsSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_data(self, users, user):
        if not user.id in users:
            users[user.id] = {}
            users[user.id]['experience'] = 0
            users[user.id]['level'] = 0

    async def add_exp(self, users, user, exp):
        users[user.id]['experience'] += exp

    async def level_up(self, users, user, channel):
        experience = users[user.id]['experience']
        lvl_start = users[user.id]['level']
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            await channel.send('{} has leveled up to level {}'.format(user.mention, lvl_end))
            users[user.id]['level'] = lvl_end

    @Cog.listener()
    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = json.load(f)

        await self.update_data(users, member)

        with open('users.json', 'r') as f:
            json.dump(users, f)

    @Cog.listener()
    async def on_message(self, message):
        # todo подключить работу с БД
        with open('users.json', 'r') as f:
            users = json.load(f)

        await self.update_data(users, message.author)
        await self.add_exp(users, message.author, random.randint(1, 15))
        await self.level_up(users, message.author, message.channel)


async def setup(bot):
    await bot.add_cog(LevelsSystem(bot))