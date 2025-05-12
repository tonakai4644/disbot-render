import discord  
from discord.ext import commands  
import random  

ROLES = ["Initiator", "Controller", "Sentinel", "Duelist", "Flex"]  

class RoleView(discord.ui.View):  
    def __init__(self):  
        super().__init__()  
        self.names = []  
        self.message = None  
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

    async def update_name_button(self, interaction: discord.Interaction):  
        if not self.names:  
            self.name_button.label = "現在の名前リスト：\nなし"  
        else:  
            self.name_button.label = "現在の名前リスト：\n" + "\n".join(self.names)  
        if self.message:  
            await self.message.edit(view=self)  

class NameModal(discord.ui.Modal, title="名前を入力"):  
    name = discord.ui.TextInput(label="名前", placeholder="例: となかい")  

    def __init__(self, view: RoleView):  
        super().__init__()  
        self.view = view  

    async def on_submit(self, interaction: discord.Interaction):  
        self.view.names.append(self.name.value)  
        await interaction.response.send_message(f"{self.name.value} を追加しました！", ephemeral=True)  
        await self.view.update_name_button(interaction)  

class Valorant(commands.Cog):  
    def __init__(self, bot):  
        self.bot = bot  

    @commands.command(name="vrole")  
    async def vrole(self, ctx, *initial_names):  
        """名前リストに引数を追加し、UIを表示"""  
        view = RoleView()  
        # 引数をリストに追加  
        view.names.extend(initial_names)  
        # 初期状態のUIのラベルも更新  
        # 例：初期の未登録状態も反映  
        # これにより名前反映とUI更新も一緒に行われる  
        # このタイミングでUIとリストが一致  
        await view.update_name_button(None)  # `interaction`の代わりにNoneを渡したい場合は`None`でも良い  
        msg = await ctx.send("名前を入力して、ロールを割り当てる", view=view)  
        view.message = msg  

async def setup(bot):  
    await bot.add_cog(Valorant(bot))
