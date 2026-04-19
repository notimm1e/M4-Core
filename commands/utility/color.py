import discord
from discord.ext import commands
from PIL import Image
import io
import colorsys

class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="color", aliases=["colour"], description="show info and swatch for a hex color")
    async def color(self, ctx, hex_code: str):
        hex_code = hex_code.lstrip("#")
        if len(hex_code) not in (3, 6) or not all(c in "0123456789abcdefABCDEF" for c in hex_code):
            return await ctx.send(embed=discord.Embed(
                description="✖ provide a valid hex code. e.g. `!color #ff4500`",
                color=0xff4500
            ))

        if len(hex_code) == 3:
            hex_code = "".join(c * 2 for c in hex_code)

        r, g, b = int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16)

        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        hsl_h = round(h * 360)
        hsl_s = round(s * 100)
        hsl_v = round(v * 100)

        img = Image.new("RGB", (200, 200), (r, g, b))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        embed = discord.Embed(title=f"#{hex_code.upper()}", color=int(hex_code, 16))
        embed.add_field(name="◈ rgb", value=f"`{r}, {g}, {b}`", inline=True)
        embed.add_field(name="◈ hsv", value=f"`{hsl_h}°, {hsl_s}%, {hsl_v}%`", inline=True)
        embed.set_thumbnail(url="attachment://color.png")

        await ctx.send(embed=embed, file=discord.File(buf, filename="color.png"))

async def setup(bot):
    await bot.add_cog(Color(bot))
