import discord
import os
import asyncio
from discord.ext import commands

API_KEY = os.getenv("OPENWEATHER_KEY")

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="weather", aliases=["w"], description="get current weather for a city")
    async def weather(self, ctx, *, city: str):
        proc = await asyncio.create_subprocess_shell(
            f'curl -s "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()

        try:
            import json
            data = json.loads(stdout.decode())
        except Exception:
            return await ctx.send(embed=discord.Embed(description="✖ failed to parse weather data.", color=0xff4500))

        if data.get("cod") == 401:
            return await ctx.send(embed=discord.Embed(description="✖ invalid api key.", color=0xff4500))
        if data.get("cod") == "404":
            return await ctx.send(embed=discord.Embed(description="✖ city not found.", color=0xff4500))
        if data.get("cod") != 200:
            return await ctx.send(embed=discord.Embed(description="✖ weather service unavailable.", color=0xff4500))

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"]
        city_name = data["name"]
        country = data["sys"]["country"]
        temp_f = round(temp * 9/5 + 32, 1)
        feels_f = round(feels * 9/5 + 32, 1)

        embed = discord.Embed(
            title=f"◈ {city_name}, {country}",
            description=f"**{desc}**",
            color=0x2b2d31
        )
        embed.add_field(name="🌡 temp", value=f"`{temp}°C / {temp_f}°F`", inline=True)
        embed.add_field(name="🤔 feels like", value=f"`{feels}°C / {feels_f}°F`", inline=True)
        embed.add_field(name="💧 humidity", value=f"`{humidity}%`", inline=True)
        embed.add_field(name="💨 wind", value=f"`{wind} m/s`", inline=True)
        embed.set_footer(text="m4-core · powered by openweathermap")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))