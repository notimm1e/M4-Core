import discord
import aiohttp
from discord.ext import commands

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="weather", aliases=["w"], description="get current weather for a city")
    async def weather(self, ctx, *, city: str):
        url = f"https://wttr.in/{city.replace(' ', '+')}?format=j1"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": "m4-core-bot"}) as resp:
                if resp.status != 200:
                    return await ctx.send(embed=discord.Embed(
                        description="✖ city not found or weather service unavailable.",
                        color=0xff4500
                    ))
                data = await resp.json()

        cur = data["current_condition"][0]
        area = data["nearest_area"][0]

        city_name = area["areaName"][0]["value"]
        country = area["country"][0]["value"]

        temp_c = cur["temp_C"]
        temp_f = cur["temp_F"]
        feels_c = cur["FeelsLikeC"]
        feels_f = cur["FeelsLikeF"]
        humidity = cur["humidity"]
        wind_kmph = cur["windspeedKmph"]
        desc = cur["weatherDesc"][0]["value"]
        visibility = cur["visibility"]

        embed = discord.Embed(
            title=f"◈ {city_name}, {country}",
            description=f"**{desc}**",
            color=0x2b2d31
        )
        embed.add_field(name="🌡 temp", value=f"`{temp_c}°C / {temp_f}°F`", inline=True)
        embed.add_field(name="🤔 feels like", value=f"`{feels_c}°C / {feels_f}°F`", inline=True)
        embed.add_field(name="💧 humidity", value=f"`{humidity}%`", inline=True)
        embed.add_field(name="💨 wind", value=f"`{wind_kmph} km/h`", inline=True)
        embed.add_field(name="👁 visibility", value=f"`{visibility} km`", inline=True)
        embed.set_footer(text="m4-core · powered by wttr.in")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))
