import discord
from discord.ext import commands
import random

ROLES = ["Initiator", "Controller", "Sentinel", "Duelist", "Flex"]

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.names = []
        # 代わりにボタンを使って名前リストを表示
        self.name_button = discord.ui.Button(label="現在の名前リスト：\nなし", style=discord.ButtonStyle.secondary, disabled=True)
        self.add_item(self.name_button)

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

    # 名前が追加された後にUIを更新するメソッド
    async def update_name_button(self):
        if not self.names:
            self.name_button.label = "現在の名前リスト：\nなし"
        else:
            self.name_button.label = "現在の名前リスト：\n" + "\n".join(self.names)
        self.stop()  # UIを更新するためにビューを更新

class NameModal(discord.ui.Modal, title="名前を入力"):
    name = discord.ui.TextInput(label="名前", placeholder="例: となかい")

    def __init__(self, view: RoleView):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        self.view.names.append(self.name.value)
        await interaction.response.send_message(f"{self.name.value} を追加しました！", ephemeral=True)
        # 名前を追加後にラベルを更新
        await self.view.update_name_button()

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vrole")
    async def vrole(self, ctx):
        """UIで名前を入力してロールをランダムに割り当てる"""
        await ctx.send("名前を入力して、ロールを割り当てる", view=RoleView())

async def setup(bot):
    await bot.add_cog(Valorant(bot))
