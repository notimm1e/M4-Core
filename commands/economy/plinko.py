import discord
import random
import asyncio
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

ROWS = 6
TOTAL_COLS = 7

SLOTS = ["▼", "◈", "❖", "▲", "✦"]
SLOT_COLORS = {
    "▼": 0xff4500,
    "◈": 0xfee75c,
    "❖": 0x5865f2,
    "▲": 0xeb459e,
    "✦": 0x57f287,
}
OUTCOMES = [0.2, 0.5, 1.2, 1.5, 3.0]
SLOT_MAP = dict(zip(SLOTS, OUTCOMES))
WEIGHTS = [25, 35, 20, 15, 5]

def build_board(path_taken, current_col, row):
    lines = []
    for r in range(ROWS):
        pegs = []
        for i in range(TOTAL_COLS):
            if r < row:
                pegs.append("•" if i == path_taken[r] else "·")
            elif r == row:
                pegs.append("⬤" if i == current_col else "·")
            else:
                pegs.append("·")
        lines.append("  ".join(pegs))
    lines.append("—" * (TOTAL_COLS * 3 - 2))
    lines.append("  ".join(SLOTS))
    return "\n".join(lines)

class Plinko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="plinko")
    async def plinko(self, ctx, amount: int):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        if amount <= 0:
            return await ctx.send("Amount must be greater than zero.")

        if amount > data[user_id]["wallet"]:
            return await ctx.send(embed=discord.Embed(
                description="⊘ insufficient cores.", color=0xff4500
            ))

        slot_symbol = random.choices(SLOTS, weights=WEIGHTS)[0]
        multiplier = SLOT_MAP[slot_symbol]
        final_board_col = SLOTS.index(slot_symbol) + 1

        current_col = 3
        path = []
        for r in range(ROWS):
            path.append(current_col)
            if r < ROWS - 1:
                if current_col < final_board_col:
                    current_col += random.choices([1, 0], weights=[75, 25])[0]
                elif current_col > final_board_col:
                    current_col -= random.choices([1, 0], weights=[75, 25])[0]
                else:
                    current_col += random.choices([-1, 0, 1], weights=[20, 60, 20])[0]
                current_col = max(0, min(TOTAL_COLS - 1, current_col))

        embed = discord.Embed(title="╼ plinko ╾", color=0x2b2d31)
        message = await ctx.send(embed=embed)

        for r in range(ROWS):
            board = build_board(path, path[r], r)
            embed.description = f"```\n{board}\n```"
            await message.edit(embed=embed)
            await asyncio.sleep(0.4)

        winnings = int(amount * multiplier)
        data[user_id]["wallet"] -= amount
        data[user_id]["wallet"] += winnings
        save_bank(data)

        result_text = f"bet: {amount}\nmultiplier: {multiplier}x\nwinnings: {winnings}"
        embed.description = f"```\n{build_board(path, path[-1], ROWS - 1)}\n```\n{result_text}"
        embed.color = SLOT_COLORS[slot_symbol]

        await message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Plinko(bot))