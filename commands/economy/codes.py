import discord
import msgpack
import os
from discord.ext import commands
from helpers.economy_base import load_bank, save_bank, open_account, apply_earnings
from helpers.admins_config import is_admin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODES_FILE = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "data", "codes.msgpack"))

def load_codes():
    if os.path.exists(CODES_FILE):
        try:
            with open(CODES_FILE, "rb") as f:
                data = msgpack.unpackb(f.read(), raw=False)
                return data if data else {}
        except (msgpack.UnpackException, OSError):
            pass
    return {}

def save_codes(data):
    os.makedirs(os.path.dirname(CODES_FILE), exist_ok=True)
    tmp = CODES_FILE + ".tmp"
    with open(tmp, "wb") as f:
        f.write(msgpack.packb(data, use_bin_type=True))
    os.replace(tmp, CODES_FILE)

class Codes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="issuecode")
    async def issuecode(self, ctx, code: str, amount: int, uses: int = 1000):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(
                description="⊘ unauthorized", color=0xff4500
            ))

        if amount <= 0:
            return await ctx.send(embed=discord.Embed(
                description="⊘ amount must be positive", color=0xff4500
            ))

        codes = load_codes()
        code = code.upper()

        if code in codes:
            return await ctx.send(embed=discord.Embed(
                description=f"⊘ code `{code}` already exists!", color=0xff4500
            ))

        codes[code] = {
            "amount": amount,
            "uses": uses,
            "redeemed_by": []
        }
        save_codes(codes)

        await ctx.send(embed=discord.Embed(
            description=f"√ code `{code}` issued — **⌬ {amount:,}** cores, **{uses}** use(s)",
            color=0x57f287
        ))

    @commands.command(name="redeem")
    async def redeem(self, ctx, code: str):
        codes = load_codes()
        code = code.upper()

        if code not in codes:
            return await ctx.send(embed=discord.Embed(
                description="⊘ invalid code!", color=0xff4500
            ), ephemeral=True)

        entry = codes[code]
        user_id = str(ctx.author.id)

        if user_id in [str(x) for x in entry["redeemed_by"]]:
            return await ctx.send(embed=discord.Embed(
                description="⊘ you've already redeemed this code!", color=0xff4500
            ), ephemeral=True)

        if entry["uses"] <= 0:
            return await ctx.send(embed=discord.Embed(
                description="⊘ this code has no uses remaining..", color=0xff4500
            ), ephemeral=True)

        entry["redeemed_by"].append(user_id)
        entry["uses"] -= 1
        save_codes(codes)

        data = load_bank()
        data = open_account(ctx.author.id, data)
        amount = entry["amount"]
        debt_paid, to_wallet = apply_earnings(user_id, data, amount)
        save_bank(data)

        desc = f"√ redeemed `{code}` — **⌬ {amount:,}** cores added"
        if debt_paid:
            desc += f"\n⌬ {debt_paid:,} went toward your debt"

        await ctx.send(embed=discord.Embed(description=desc, color=0x57f287))

    @commands.command(name="revokecode")
    async def revokecode(self, ctx, code: str):
        if not is_admin(ctx.author.id):
            return await ctx.send(embed=discord.Embed(
                description="⊘ unauthorized", color=0xff4500
            ))

        codes = load_codes()
        code = code.upper()

        if code not in codes:
            return await ctx.send(embed=discord.Embed(
                description=f"⊘ code `{code}` doesn't exist!", color=0xff4500
            ))

        del codes[code]
        save_codes(codes)

        await ctx.send(embed=discord.Embed(
            description=f"√ code `{code}` revoked", color=0x57f287
        ))

async def setup(bot):
    await bot.add_cog(Codes(bot))