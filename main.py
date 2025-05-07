import discord
import os
from keep import keep_alive


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'ログインしました: {self.user}')

    async def on_message(self, message):
        print(f'送信: {message.author}: {message.content}')
        if message.author == self.user:
            return

        if message.content == '$Hello':
            await message.channel.send('Hello!')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
keep_alive()

try:
    token = os.getenv("DISCORD_TOKEN")  # 環境変数名はRenderの設定に合わせて
    client.run(token)  # ✅ 修正：client を使う
except Exception as e:
    print(f"Bot実行中にエラーが発生しました: {e}")
