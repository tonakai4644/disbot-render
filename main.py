import discord
from discord.ext import commands
import os
import logging
from keep import keep_alive

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# インテント設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # 参加/退出イベントに必要

# Botインスタンス作成（コマンドプレフィックスを $ に設定）
bot = commands.Bot(command_prefix="$", intents=intents)

# Bot起動時イベント
@bot.event
async def on_ready():
    logger.info(f"ログインしました: {bot.user}")

# メンバー参加イベント
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(938403730863316992)
    if channel:
        await channel.send(f"{member.mention} さんがCROSSに参加しました！")
        logger.info(f"{member} が参加しました。")

# メンバー退出イベント
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(938403730863316992)
    if channel:
        await channel.send(f"{member.mention} さんがCROSSを去りました。")
        logger.info(f"{member} が退出しました。")

# `$Hello` コマンド
@bot.command()
async def Hello(ctx):
    import socket
    hostname = socket.gethostname()
    await ctx.send(f"Hello from {hostname}!")
    logger.info(f"{ctx.author} が $Hello を使用しました（{hostname}）")



# サーバー起動（keep_alive関数を実行してからBotを起動）
keep_alive()

try:
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("TOKENが環境変数に設定されていません。")
    bot.run(token)
except Exception as e:
    logger.exception(f"Bot実行中にエラーが発生しました: {e}")
