import random
import discord
import requests
from discord import app_commands

from discord.ext import commands
from bs4 import BeautifulSoup as bs


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class JankenButtons(discord.ui.View):
        def __init__(self, embed):
            super().__init__()
            self.__answers = ['Камень', 'Ножницы', 'Бумага']
            self.__user_choice = None
            self.__embed = embed

        async def __edit_message(self, interaction):
            answer = random.choice(self.__answers)
            victory = None

            if self.__user_choice == 'Камень' and answer == 'Ножницы':
                victory = True

            elif self.__user_choice == 'Ножницы' and answer == 'Бумага':
                victory = True

            elif self.__user_choice == 'Бумага' and answer == 'Камень':
                victory = True

            elif self.__user_choice is answer:
                victory = None

            else:
                victory = False

            if victory:
                await interaction.response.edit_message(content=None,
                                                        view=None,
                                                        embed=discord.Embed(
                                                            color=self.__embed.color,
                                                            title=self.__embed.title,
                                                            description=f"{self.__embed.description} \n"
                                                                        f"Ты выбрал `{self.__user_choice}`, а я выбрал `{answer}` \n"
                                                                        "Впервые в своей жизни ты победил..."))
            elif not victory and victory is not None:
                await interaction.response.edit_message(content=None,
                                                        view=None,
                                                        embed=discord.Embed(
                                                            color=self.__embed.color,
                                                            title=self.__embed.title,
                                                            description=f"{self.__embed.description} \n"
                                                                        f"Ты выбрал `{self.__user_choice}`, а я выбрал `{answer}` \n"
                                                                        "Ну да. Ты проиграл, как всегда"))

            else:
                await interaction.response.edit_message(content=None,
                                                        view=None,
                                                        embed=discord.Embed(
                                                            color=self.__embed.color,
                                                            title=self.__embed.title,
                                                            description=f"{self.__embed.description} \n"
                                                                        f"Ты выбрал `{self.__user_choice}`, а я выбрал `{answer}` \n"
                                                                        "Ничья. Давай ещё раз"))

        @discord.ui.button(label="Камень", emoji="🗿", style=discord.ButtonStyle.blurple)
        async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.__user_choice = "Камень"
            await self.__edit_message(interaction)

        @discord.ui.button(label="Ножницы", emoji="✂️", style=discord.ButtonStyle.red)
        async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.__user_choice = "Ножницы"
            await self.__edit_message(interaction)

        @discord.ui.button(label="Бумага", emoji="📄", style=discord.ButtonStyle.gray)
        async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.__user_choice = "Бумага"
            await self.__edit_message(interaction)

    @app_commands.command()
    async def janken(self, interaction: discord.Interaction):
        """Камень ножницы бумага!"""
        description = 'Сыграй со мной в камень ножницы бумагу! выбери один из вариантов ниже:'
        embed = discord.Embed(color=0xffcd4c, title=f'{interaction.user}: Камень Ножницы Бумага',
                              description=description)
        await interaction.response.send_message(embed=embed, view=self.JankenButtons(embed=embed))

    @app_commands.command()
    async def slots(self, interaction: discord.Interaction):
        """Азино три топора"""
        author_id = str(interaction.user.id)

        symbols = ['🍒', '🔔', '7️⃣', '👑', '☠️']

        slot = [0, 1, 2]

        for i in range(3):
            slot[i] = symbols[random.randint(0, 3)]

        is_same = True if slot[0] == slot[1] == slot[2] else False

        if is_same and symbols[4] in slot:
            footer = 'Лузер! Ваш баланс обнулён'
        elif is_same and symbols[3] in slot:
            footer = '+ 5 000 баксов на ваш счёт'
        elif is_same and symbols[2] in slot:
            footer = '+ 10 000 баксов на ваш счёт'
        elif is_same and symbols[1] in slot:
            footer = '+ 15 000 баксов на ваш счёт'
        elif is_same and symbols[0] in slot:
            footer = 'ДЖЕКПОТ!!! + 1 000 000 баксов на ваш счёт'
        elif symbols[0] == slot[0] == slot[1] or slot[0] == slot[2] == symbols[0] or slot[1] == slot[2] == symbols[0]:
            footer = '+ 3 500 баксов на ваш счёт'
        elif symbols[0] in slot:
            footer = '+ 1 500 баксов на ваш счёт'
        else:
            footer = 'Ничего('
        embed = discord.Embed(color=0x36c600, title='🎰 Slots Azino777',
                              description=str(slot[0]) + str(slot[1]) + str(slot[2]))
        embed.set_footer(text=footer, icon_url="https://i.imgur.com/uZIlRnK.png")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def joke(self, interaction: discord.Interaction):
        """Парсит анекдот из сайта, и делится им с тобой"""
        joke_website = "https://baneks.ru/"
        joke_number = str(random.randint(1, 1142))

        joke_url = joke_website + joke_number
        request = requests.get(joke_url)
        soup = bs(request.text, "html.parser")

        parsed = soup.find_all("article")
        for jokes in parsed:
            embed = discord.Embed(color=0x33bbff, title=f"📋 Анекдот #{joke_number}",
                                  description=jokes.p.text)
            embed.set_footer(text="")
            await interaction.response.send_message("А вот и анекдот!", ephemeral=True, delete_after=5)
            message = await interaction.channel.send(embed=embed)

            emojis = ['🤣', '😐', '💩', '🪗']
            for emoji in emojis:
                await message.add_reaction(emoji)


async def setup(bot):
    await bot.add_cog(Fun(bot))