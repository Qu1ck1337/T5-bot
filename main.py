import asyncio
import os

import discord
from discord.ext import commands
from discord import app_commands

from tools.bcolors import bcolors
from tools.console import console

from dotenv import load_dotenv

# Loading .env file
load_dotenv()


intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix="!", intents=intents)


# Called when the client is done preparing the data received from Discord.
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name="is under development"))

    console(bcolors.OKCYAN, "Enabled commands:")
    for command in bot.tree.get_commands():
        console(bcolors.OKCYAN, "-\t/" + command.name, f'\t(NSFW: {command.nsfw})')
    console(bcolors.OKCYAN, f"{len(bot.tree.get_commands())} commands")

    console(bcolors.OKGREEN, "Bot is ready")


@bot.tree.error
async def error(interaction, error):
    ' Command on Cooldown '
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.send(f":stopwatch: Command is on Cooldown for **{error.retry_after:.2f}** seconds.")
        ' Missing Permissions '
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.send(f":x: You can't use that command.")
        ' Missing Arguments '
    elif isinstance(error, commands.MissingRequiredArgument):
        await interaction.send(f":x: Required arguments aren't passed.")
        ' Command not found '
    elif isinstance(error, app_commands.CommandNotFound):
        pass
        ' Any Other Error '
    else:
        # ss = get(bot.guilds, id=1185712613905141852)
        # report = get(ss.text_channels, id=1197159353065680926)
        # embed = discord.Embed(title='An Error has occurred', description=f'Error: \n `{error}`',
        #                       timestamp=interaction.created_at, color=242424)
        # await report.send(embed=embed)
        print(error)


# Load extensions from ./cogs
async def load_extensions():
    console(bcolors.OKBLUE, "Loading extensions:")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            console("-\t" + bcolors.OKBLUE + filename)
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        console(bcolors.ENDC, "Starting bot via token from .env")
        try:
            await bot.start(os.getenv('TOKEN'))
        except discord.LoginFailure as e:
            console(bcolors.WARNING, e)
            console(bcolors.FAIL, "Be sure you placed file .env with right token in current directory")


asyncio.run(main())