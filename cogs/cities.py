import discord
import codecs
from discord.ext import commands
import datetime
import json
import discord
from discord import app_commands
from discord.ext import commands
import random


client = discord.Client(intents=discord.Intents().all())

f = open("cogs\\recources\\cities.txt", "r", encoding='utf-8')
list_of_cities = []
for line in f:
    if line != "":
        list_of_cities.append(line.lower().replace('\n', ''))
f.close()


class Cities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cities = []
        self.last_letter = ""
        self.check = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        elif message.content == "!play cities" and self.check == False:
            await message.channel.send("Let's play, I'll start")
            number = random.randint(0, len(list_of_cities))
            now_city = list_of_cities[number]
            self.last_letter = now_city[-1]
            list_of_cities.remove(now_city)
            await message.channel.send(f"{now_city.title()}")
            await message.channel.send("Your turn")
            self.check = True
        elif message.content == "!stop cities" and self.check == True:
            await message.channel.send("Play finished")
            self.check = False
        elif self.check == True:

            player_city = message.content.lower()
            
            if player_city not in list_of_cities:
                await message.channel.send("Your city doesn't exist or has already appeared")
                await message.channel.send("Try again")
            elif player_city[0] != self.last_letter:
                await message.channel.send(f"Your city needs to start with letter '{self.last_letter}'")
            else:
                list_of_cities.remove(player_city)
                start_letter = player_city[-1]
                for i in list_of_cities:
                    if (i[0] == start_letter):
                        await message.channel.send(f"{i.title()}")
                        self.last_letter = i[-1]
                        list_of_cities.remove(i)
                        await message.channel.send("Your turn")
                        return
                await message.channel.send("You won")
                self.check = False

                
        
        

async def setup(bot):
    await bot.add_cog(Cities(bot))
