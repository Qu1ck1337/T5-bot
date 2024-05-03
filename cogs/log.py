import discord
from discord.app_commands import commands
from discord.ext.commands import Cog


LOGGER_CHANNEL = 1231233871811575849


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(title="{} deleted a message".format(message.author.name),
                              description="", color=0xFF0000)
        embed.add_field(name=message.content, value="This is the message that he has deleted",
                        inline=True)
        channel = self.bot.get_channel(LOGGER_CHANNEL)
        await channel.send(channel, embed=embed)

    @Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        embed = discord.Embed(title="{} edited a message".format(message_before.author.name),
                              description="", color=0xFF0000)
        embed.add_field(name=message_before.content, value="This is the message before any edit",
                        inline=True)
        embed.add_field(name=message_after.content, value="This is the message after the edit",
                        inline=True)
        channel = self.bot.get_channel(LOGGER_CHANNEL)
        await channel.send(channel, embed=embed)


    # todo Сделать другие обработчики ивентов (присоединение в голосовой канал, кик, бан)


async def setup(bot):
    await bot.add_cog(Logger(bot))