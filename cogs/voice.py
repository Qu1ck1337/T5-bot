import discord
from discord import app_commands, ui
from discord.ext import commands
from tools import DB


class Voice(commands.Cog):
    def __init__(self, bot):
        self.temporary_channels = []
        self.bot = bot

    # модальное окно для изменения названия канала
    class NameModal(ui.Modal, title="New Channel Name"):
        name = ui.TextInput(label="New Channel Name", placeholder="Channel name", style=discord.TextStyle.short)

        async def on_submit(self, interaction: discord.Interaction):
            voice_channel = interaction.guild.get_channel(interaction.channel_id)
            await voice_channel.edit(name=self.name.value)
            await interaction.response.send_message(f"Channel name changed to {self.name}", ephemeral=True)
            DB.cursor.execute(f"UPDATE voice_rooms SET room_name = '{self.name.value}' WHERE user_id = {interaction.user.id}")
            DB.conn.commit()
            
    # модальное окно для изменения лимита канала
    class LimitModal(ui.Modal, title="New Channel Limit"):
        limit = ui.TextInput(label="New Channel Limit", placeholder="0 for unlimited", style=discord.TextStyle.short)

        async def on_submit(self, interaction: discord.Interaction):
            voice_channel = interaction.guild.get_channel(interaction.channel_id)
            await voice_channel.edit(user_limit=int(self.limit.value))
            await interaction.response.send_message(f"Channel limit changed to {self.limit}", ephemeral=True)
            DB.cursor.execute(f"UPDATE voice_rooms SET participants_limit = '{self.limit.value}' WHERE user_id = {interaction.user.id}")
            DB.conn.commit()
        
    # меню выбора команд в голосовом чате
    class SettingsDropdown(discord.ui.Select):
        def __init__(self):
            options=[
                discord.SelectOption(label="Name", description="Change channel name", emoji="📝"),
                discord.SelectOption(label="Limit", description="Change channel limit", emoji="🔢")
            ]

            super().__init__(placeholder="Select an option", options=options, min_values=1, max_values=1)

        
        async def callback(self, interaction: discord.Interaction):
            voice_channel = interaction.channel_id
            guild = interaction.guild
            
            if self.values[0] == "Name":
                await interaction.response.send_modal(Voice.NameModal())
                
            elif self.values[0] == "Limit":
                await interaction.response.send_modal(Voice.LimitModal())
                

    class SettingsView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(Voice.SettingsDropdown())

    #создание личного канала через Join to create VC
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        possible_channel_name = f"{member.display_name}'s VC"
        possible_chanel_limit = 0

        if before.channel:
            if before.channel.id in self.temporary_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    self.temporary_channels.remove(before.channel.id)

        try:
            if after.channel.name == "Join to create VC":
                DB.cursor.execute(f"SELECT id FROM users WHERE id={member.id}")
                if not DB.cursor.fetchone():
                    DB.cursor.execute(f"INSERT INTO users VALUES ({member.id})")
                    DB.conn.commit()

                DB.cursor.execute(f"SELECT room_name, participants_limit FROM voice_rooms WHERE user_id = {member.id}")
                data = DB.cursor.fetchone()
                if data is not None:
                    possible_channel_name = data[0]
                    possible_chanel_limit = data[1]
                else:
                    query = "INSERT INTO voice_rooms (user_id, room_name, participants_limit) VALUES (%s, %s, %s)"
                    DB.cursor.execute(query, (member.id, possible_channel_name, 0))
                    DB.conn.commit()

                new_channel = await after.channel.clone(name=possible_channel_name)
                await new_channel.edit(user_limit=possible_chanel_limit)

                await member.move_to(new_channel)
                self.temporary_channels.append(new_channel.id)
                view = self.SettingsView()
                await new_channel.send("Choose setting for this voice channel",view=view)
        except Exception as ex:
            print(ex)

    #создание канала Join to creaete VC через команду
    @app_commands.command(name="create_vc", description="Create a voice channel")

    @commands.has_permissions(manage_channels=True)
    async def create_vc(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Voice Channels")
        await guild.create_voice_channel(name="Join to create VC", category=category)
        await interaction.response.send_message("Voice channel created", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Voice(bot))