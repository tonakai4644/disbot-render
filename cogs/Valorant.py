# valorant.py (cogs/valorant.py)
import discord
from discord.ext import commands
import random

ROLES = ["Initiator", "Controller", "Sentinel", "Duelist", "Flex"]

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.names = []

    @discord.ui.button(label="名前を追加", style=discord.ButtonStyle.primary)
    async def add_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = NameModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="ランダムにロールを割り当てる", style=discord.ButtonStyle.success)
    async def assign_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.names:
            await interaction.response.send_message("名前が入力されていません。", ephemeral=True)
            return

        random.shuffle(ROLES)
        result = ""
        for i, name in enumerate(self.names):
            role = ROLES[i % len(ROLES)]
            result += f"{name}: {role}\n"

        await interaction.response.send_message(f"```{result}```")

class NameModal(discord.ui.Modal, title="名前を入力"):
    name = discord.ui.TextInput(label="名前", placeholder="例: となかい")

    def __init__(self, view: RoleView):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        self.view.names.append(self.name.value)
        await interaction.response.send_message(f"{self.name.value} を追加しました！", ephemeral=True)


class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vrole")
    async def vrole(self, ctx):
        """UIで名前を入力してロールをランダムに割り当てる"""
        await ctx.send("名前を入力して、ロールを割り当てましょう！", view=RoleView())

async def setup(bot):
    await bot.add_cog(Valorant(bot))
