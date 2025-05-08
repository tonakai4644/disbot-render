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

    async def on_member_join(self, member):
        # 固定チャンネルにメッセージを送る
        channel = self.get_channel(938403730863316992)
        if channel:
            await channel.send(f'{member.mention} さんがCROSSに参加しました！')

# intents設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # メンバー参加検出に必要

client = MyClient(intents=intents)
keep_alive()

try:
    token = os.getenv("TOKEN")
    client.run(token)
except Exception as e:
    print(f"Bot実行中にエラーが発生しました: {e}")
