import discord
import random
import asyncio
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

ROWS = 6
SLOTS = ["💀", "⚡", "✨", "🔥", "💎"]
SLOT_COLORS = {
    "💀": 0xff4500,
    "⚡": 0xfee75c,
    "✨": 0x5865f2,
    "🔥": 0xeb459e,
    "💎": 0x57f287,
}
OUTCOMES = [0.2, 0.5, 1.2, 1.5, 3.0]
SLOT_MAP = dict(zip(SLOTS, OUTCOMES))
WEIGHTS = [25, 35, 20, 15, 5]

def build_board(path_taken, current_col, row, total_cols=7):
    lines = []
    for r in range(ROWS):
        if r < row:
            # already passed — show pegs with trail
            col = path_taken[r]
            pegs = ["◆" if i == col else "◇" for i in range(total_cols)]
            lines.append(" ".join(pegs))
        elif r == row:
            # ball is here
            pegs = ["◇"] * total_cols
            pegs[current_col] = "●"
            lines.append(" ".join(pegs))
        else:
            lines.append("  ".join(["◇"] * total_cols))
    # slot row
    slot_row = " ".join(SLOTS)
    lines.append(slot_row)
    return "\n".join(lines)

class Plinko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="plinko")
    async def plinko(self, ctx, amount: int):
        data = load_bank()
        data = open_account(ctx.author.id, data)
        user_id = str(ctx.author.id)

        if amount <= 0 or amount > data[user_id]["wallet"]:
            return await ctx.send(embed=discord.Embed(
                description="⊘ insufficient cores.", color=0xff4500
            ))

        # Pick final slot first so we can animate toward it
        slot_emoji = random.choices(SLOTS, weights=WEIGHTS)[0]
        multiplier = SLOT_MAP[slot_emoji]
        final_col = SLOTS.index(slot_emoji)  # 0-4, map to board cols
        # board has 7 cols (indices 0-6), slots are at 1,2,3,4,5
        final_board_col = final_col + 1

        # Simulate path: start at col 3 (center), drift toward final_board_col
        col = 3
        path = []
        for r in range(ROWS):
            path.append(col)
            if r < ROWS - 1:
                # bias toward final col
                target = final_board_col
                if col < target:
                    col += random.choices([1, 0], weights=[70, 30])[0]
                elif col > target:
                    col -= random.choices([1, 0], weights=[70, 30])[0]
                else:
                    col += random.choices([-1, 0, 1], weights=[30, 40, 30])[0]
                col = max(0, min(6, col))

        # Initial embed
        embed = discord.Embed(
            title="╼ plinko ╾",
            description=f"```\n{build_board(path, 3, 0)}\n```\nbet: **⌬ {amount:,}**",
            color=0x5865f2
        )
        msg = await ctx.send(embed=embed)

        # Animate ball dropping
        for r in range(ROWS):
            await asyncio.sleep(0.6)
            board = build_board(path, path[r], r)
            embed.description = f"```\n{board}\n```\nbet: **⌬ {amount:,}**"
            await msg.edit(embed=embed)

        # Final result
        await asyncio.sleep(0.6)
        winnings = int(amount * multiplier)
        net = winnings - amount
        data[user_id]["wallet"] = data[user_id]["wallet"] - amount + winnings
        save_bank(data)

        result_color = SLOT_COLORS[slot_emoji]
        result_sign = "+" if net >= 0 else ""
        final_embed = discord.Embed(
            title=f"╼ plinko · {slot_emoji} ╾",
            description=(
                f"```\n{build_board(path, final_board_col, ROWS)}\n```"
                f"multiplier: **{multiplier}x**\n"
                f"payout: **⌬ {winnings:,}** ({result_sign}{net:,})\n"
                f"wallet: **⌬ {data[user_id]['wallet']:,}**"
            ),
            color=result_color
        )
        await msg.edit(embed=final_embed)

async def setup(bot):
    await bot.add_cog(Plinko(bot))
