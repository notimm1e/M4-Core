import discord
from discord.ext import commands
import qrcode
import io

class QR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="qr", description="generate a qr code from text or a url")
    async def qr(self, ctx, *, text: str):
        img = qrcode.make(text)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        await ctx.send(
            embed=discord.Embed(description=f"◈ qr for: `{text[:80]}`", color=0x2b2d31),
            file=discord.File(buf, filename="qr.png")
        )

async def setup(bot):
    await bot.add_cog(QR(bot))
