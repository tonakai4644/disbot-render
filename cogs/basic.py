from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Hello(self, ctx):
        await ctx.send("Hello!")
        logger.info(f"{ctx.author} が $Hello を使用しました。")

async def setup(bot):
    await bot.add_cog(Basic(bot))
