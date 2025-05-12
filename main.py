import discord
from discord.ext import commands
import os
import logging
from keep import keep_alive

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"ログインしました: {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(938403730863316992)
    if channel:
        await channel.send(f"{member.mention} さんがCROSSに参加しました！")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(938403730863316992)
    if channel:
        await channel.send(f"{member.mention} さんがCROSSを去りました。")

# コグを読み込む
@bot.event
async def setup_hook():
    await bot.load_extension("cogs.basic")
    await bot.load_extension("cogs.valorant")
    await bot.load_extension("cogs.rpg")

# keep_alive を使ってRender維持
keep_alive()

try:
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("TOKENが設定されていません")
    bot.run(token)
except Exception as e:
    logger.exception(f"Bot実行中にエラーが発生しました: {e}")
