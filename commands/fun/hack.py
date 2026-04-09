import discord
import random
import asyncio
from discord.ext import commands

DEVICES = ["MacBook Pro 2021", "Dell XPS 15", "ThinkPad X1 Carbon", "Razer Blade 15", "HP Spectre x360", "Surface Pro 9"]
OS_LIST = ["Windows 11 Home", "Ubuntu 22.04 LTS", "macOS Ventura 13.2", "Arch Linux (btw)", "Fedora 38"]
STREETS = ["Oak Street", "Maple Avenue", "Pine Road", "Cedar Lane", "Elm Boulevard", "Birch Court"]
CITIES = ["Springfield", "Shelbyville", "Ogdenville", "North Haverbrook", "Brockway", "Capital City"]
STATES = ["TX", "CA", "NY", "FL", "OH", "WA"]
PASSWORDS = ["hunter2", "password123", "iloveyou", "qwerty", "letmein", "abc123", "monkey", "dragon", "sunshine", "football"]
BANKS = ["First National Bank", "Shelbyville Credit Union", "Springfield Savings", "Ogden Federal", "North Haverbrook Bank"]

def fake_ip():
    return f"{random.randint(100,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def fake_mac():
    return ":".join(f"{random.randint(0,255):02x}" for _ in range(6))

class hack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hack")
    async def hack(self, ctx, member: discord.Member):
        ip = fake_ip()
        mac = fake_mac()
        device = random.choice(DEVICES)
        os_name = random.choice(OS_LIST)
        street = f"{random.randint(1,9999)} {random.choice(STREETS)}"
        city = random.choice(CITIES)
        state = random.choice(STATES)
        zipcode = random.randint(10000, 99999)
        bank = random.choice(BANKS)
        balance = round(random.uniform(2.50, 47.99), 2)
        passwords = random.sample(PASSWORDS, 3)

        steps = [
            f"⟳ initializing hack sequence on {member.mention}...",
            f"⟳ resolving ip address... `{ip}`",
            f"⟳ pinging device... `{device}` running `{os_name}`",
            f"⟳ spoofing mac address... `{mac}`",
            f"⟳ triangulating location... `{street}, {city}, {state} {zipcode}`",
            f"⟳ breaching password vault...",
            f"⟳ cracking encryption...",
            f"√ hack complete.",
        ]

        embed = discord.Embed(title="⟳ hacking...", description=steps[0], color=discord.Color.red())
        msg = await ctx.send(embed=embed)

        for step in steps[1:]:
            await asyncio.sleep(1.2)
            embed.description = step
            await msg.edit(embed=embed)

        await asyncio.sleep(1)

        result_embed = discord.Embed(
            title=f"√ hacked {member.display_name}",
            color=discord.Color.red()
        )
        result_embed.add_field(name="ip address", value=f"`{ip}`", inline=True)
        result_embed.add_field(name="mac address", value=f"`{mac}`", inline=True)
        result_embed.add_field(name="device", value=f"`{device}`", inline=True)
        result_embed.add_field(name="os", value=f"`{os_name}`", inline=True)
        result_embed.add_field(name="location", value=f"`{street}, {city}, {state} {zipcode}`", inline=False)
        result_embed.add_field(name="bank", value=f"`{bank}` · balance: `${balance}`", inline=False)
        result_embed.add_field(name="passwords found", value="\n".join(f"`{p}`" for p in passwords), inline=False)
        result_embed.set_thumbnail(url=member.display_avatar.url)
        result_embed.set_footer(text="totally real. 100% legit. not fake at all.")
        await msg.edit(embed=result_embed)

    @hack.error
    async def hack_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title="✖ missing target", description="usage: `!hack @member`", color=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(hack(bot))
