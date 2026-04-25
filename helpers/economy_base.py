import msgpack
import os
import time
import asyncio
import discord

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANK_FILE = os.path.join(BASE_DIR, "bank.msgpack")

def load_bank():
    if os.path.exists(BANK_FILE):
        try:
            with open(BANK_FILE, "rb") as f:
                data = msgpack.unpack(f, raw=False)
                return data if data else {}
        except (msgpack.UnpackException, OSError):
            pass
    return {}

def save_bank(data):
    tmp = BANK_FILE + ".tmp"
    with open(tmp, "wb") as f:
        msgpack.pack(data, f, use_bin_type=True)
    os.replace(tmp, BANK_FILE)
    
def open_account(user_id, data):
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "wallet": 100,
            "bank": 0,
            "debt": 0,
            "last_work": 0,
            "last_beg": 0,
            "last_daily": 0,
            "last_crime": 0,
            "last_rob": 0,
        }
        save_bank(data)
    else:
        changed = False
        for key in ("last_work", "last_beg", "last_daily", "last_crime", "last_rob"):
            if key not in data[user_id]:
                data[user_id][key] = 0
                changed = True
        if "debt" not in data[user_id]:
            data[user_id]["debt"] = 0
            changed = True
        if changed:
            save_bank(data)
    return data

def get_cooldown(user_id, data, key, seconds):
    current_time = time.time()
    last_time = data[str(user_id)].get(key, 0)
    remaining = (last_time + seconds) - current_time
    return max(0, round(remaining))

def set_cooldown(user_id, data, key):
    data[str(user_id)][key] = time.time()

def apply_loss(user_id, data, amount):
    uid = str(user_id)
    wallet = data[uid]["wallet"]
    if amount <= wallet:
        data[uid]["wallet"] -= amount
    else:
        data[uid]["debt"] += amount - wallet
        data[uid]["wallet"] = 0

def apply_earnings(user_id, data, amount):
    uid = str(user_id)
    debt = data[uid]["debt"]
    if debt > 0:
        if amount >= debt:
            data[uid]["debt"] = 0
            data[uid]["wallet"] += amount - debt
            return debt, amount - debt
        else:
            data[uid]["debt"] -= amount
            return amount, 0
    else:
        data[uid]["wallet"] += amount
        return 0, amount

async def debt_prompt(ctx, bot, data, user_id):
    uid = str(user_id)
    debt = data[uid]["debt"]
    if debt == 0:
        return data

    bank = data[uid]["bank"]

    if bank > 0:
        desc = (
            f"you're **⌬ {debt:,}** in debt, and you have **⌬ {bank:,}** in your bank\n\n"
            f"would you like to pay off your debt with your bank balance to the extent possible?"
        )
    else:
        desc = f"you're **⌬ {debt:,}** in debt.\n\ncontinuing..."

    embed = discord.Embed(title="◈ in debt", description=desc, color=0xff4500)
    msg = await ctx.send(embed=embed)

    if bank == 0:
        return data

    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    def check(reaction, user):
        return (
            user.id == ctx.author.id
            and reaction.message.id == msg.id
            and str(reaction.emoji) in ("✅", "❌")
        )

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(embed=discord.Embed(
            title="◈ in debt",
            description="⧖ timed out, continuing in debt",
            color=0xff4500
        ))
        try:
            await msg.clear_reactions()
        except:
            pass
        return data

    try:
        await msg.clear_reactions()
    except:
        pass

    if str(reaction.emoji) == "✅":
        paid = min(bank, debt)
        data[uid]["bank"] -= paid
        data[uid]["debt"] -= paid
        remaining = data[uid]["debt"]
        if remaining == 0:
            result = f"√ paid off **⌬ {paid:,}** — debt cleared!"
        else:
            result = f"√ paid **⌬ {paid:,}** from bank — **⌬ {remaining:,}** still owed"
        await msg.edit(embed=discord.Embed(title="◈ in debt", description=result, color=0x57f287))
        save_bank(data)
    else:
        await msg.edit(embed=discord.Embed(
            title="◈ in debt",
            description=f"✖ staying in debt, **⌬ {debt:,}** owed",
            color=0xff4500
        ))

    return data
