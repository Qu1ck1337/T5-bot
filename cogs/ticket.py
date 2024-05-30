import discord
from discord import app_commands
from discord import ui
from discord.ext import commands


class Ticket(commands.Cog):
    class MyModal(ui.Modal, title="Report"):
        name = ui.TextInput(label="Enter your name", placeholder="My name is...", style=discord.TextStyle.short)
        about = ui.TextInput(label="Describe the situation", placeholder="The problem is...", style=discord.TextStyle.long)

        async def on_submit(self, interaction: discord.Interaction):
            embed = discord.Embed(title="New Report", description=f"**Name:** {self.name} ({interaction.user.name})\n**About: **{self.about}\nDo you want to reply on this report?", color=discord.Color.orange())
            channel = interaction.guild.get_channel(1245747675480064071)
            await channel.send(embed=embed, view=Ticket.Cf())
            await interaction.response.send_message(f"Thank you for reporting, **{interaction.user.mention}**!", ephemeral=True)
            global user
            user = interaction.user

    async def yes_or_no(self, interaction: discord.Interaction, choice):
        if choice == "Yes":
            guild = interaction.guild
            member = user
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True),
            }
            channel = await guild.create_text_channel(name=f"ticket-{member.display_name}", overwrites=overwrites)
            await interaction.message.delete()
            await interaction.response.send_message(f"Your ticket has been created at {channel.mention}")
            await channel.send(f"Hi, {member.mention}! Can you, please, provide more information about your report?\nIf you want to close this ticket, please click the button below.", view=Ticket.Cf3())
        else:
            await interaction.response.send_message("Your ticket has been cancelled.", ephemeral=True)
            await interaction.message.delete()


    class PersistentViewBot(commands.Bot):
        def __init__(self):
            intents = discord.Intents().all()
            super().__init__(command_prefix=commands.when_mentioned_or("."), intents=intents)
        async def setup_hook(self) -> None:
            self.add_view(Ticket.Cf())

    class PersistentViewBot2(commands.Bot):
        def __init__(self):
            intents = discord.Intents().all()
            super().__init__(command_prefix=commands.when_mentioned_or("."), intents=intents)
        async def setup_hook(self) -> None:
            self.add_view(Ticket.Cf2())

    class PersistentViewBot3(commands.Bot):
        def __init__(self):
            intents = discord.Intents().all()
            super().__init__(command_prefix=commands.when_mentioned_or("."), intents=intents)
        async def setup_hook(self) -> None:
            self.add_view(Ticket.Cf3())
            
    class Cf(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="1")
        async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
            await Ticket.yes_or_no(self, interaction, choice="Yes")

        @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="2")
        async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
            await Ticket.yes_or_no(self, interaction, choice="No")

    class Cf2(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Create a ticket", style=discord.ButtonStyle.green, custom_id="3")
        async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_modal(Ticket.MyModal())

    class Cf3(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Close ticket", style=discord.ButtonStyle.red, custom_id="4")
        async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.channel.delete()

    @app_commands.command(name="report", description="Create a message with report by ticket system")
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_message("If you want to create a ticket, click the button below.", view=Ticket.Cf2())


async def setup(bot):
    await bot.add_cog(Ticket(bot))