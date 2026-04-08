import discord
import random
import asyncio
from discord.ext import commands
from commands.economy.economy_base import load_bank, save_bank, open_account

ROWS = 6
SLOTS = ["▼", "◈", "❖", "▲", "✦"]
TOTAL_COLS = len(SLOTS) * 2 - 1

SLOT_COLORS = {
    "▼": 0xff4500,
    "◈": 0xfee75c,
    "❖": 0x5865f2,
    "▲": 0xeb459e,
    "✦": 0x57f287,
}

# risk modes
RISK_MODES = {
    "low": {
        "multipliers": [0.5, 0.8, 1.0, 1.2, 1.5],
        "weights":     [10, 25, 30, 25, 10],
    },
    "medium": {
        "multipliers": [0.2, 0.5, 1.2, 1.5, 3.0],
        "weights":     [25, 35, 20, 15, 5],
    },
    "high": {
        "multipliers": [0.0, 0.2, 1.5, 3.0, 5.0],
        "weights":     [35, 30, 20, 10, 5],
    }
}

RISK_EMOJIS = {
    "🟢": "low",
    "🟡": "medium",
    "🔴": "high"
}


def build_board(path_taken, current_col, row):
    lines = []

    for r in range(ROWS):
        pegs = []
        for c in range(TOTAL_COLS):
            if r < row:
                if c == path_taken[r]:
                    if r > 0:
                        prev = path_taken[r - 1]
                        if prev < c:
                            pegs.append("╲")
                        elif prev > c:
                            pegs.append("╱")
                        else:
                            pegs.append("│")
                    else:
                        pegs.append("│")
                else:
                    pegs.append("·")

            elif r == row:
                pegs.append("⬤" if c == current_col else "·")
            else:
                pegs.append("·")

        lines.append("  ".join(pegs))

    # bottom line
    lines.append("═" * (TOTAL_COLS * 3 - 2))

    # evenly spaced slots across full width
    width = TOTAL_COLS * 3 - 2
    gap = (width - len(SLOTS)) // (len(SLOTS) - 1)

    slot_line = ""
    for i, s in enumerate(SLOTS):
        slot_line += s
        if i < len(SLOTS) - 1:
            slot_line += " " * gap

    lines.append(slot_line)
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
            return await ctx.send("amount must be greater than zero.")

        if amount > data[user_id]["wallet"]:
            return await ctx.send(embed=discord.Embed(
                description="⊘ insufficient cores.",
                color=0xff4500
            ))

        # risk select embed
        embed = discord.Embed(
            title="╼ plinko ╾",
            description=(
                "select risk mode\n\n"
                f"bet: {amount}\n"
                f"wallet: {data[user_id]['wallet']} cores"
            ),
            color=0x2b2d31
        )

        message = await ctx.send(embed=embed)

        for emoji in RISK_EMOJIS:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == message.id
                and str(reaction.emoji) in RISK_EMOJIS
            )

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=30.0, check=check
            )
        except asyncio.TimeoutError:
            return await message.edit(embed=discord.Embed(
                description="⌛ timed out selecting risk.",
                color=0xed4245
            ))

        risk = RISK_EMOJIS[str(reaction.emoji)]
        mode = RISK_MODES[risk]

        multipliers = mode["multipliers"]
        weights = mode["weights"]

        multiplier = random.choices(multipliers, weights=weights)[0]
        slot_index = multipliers.index(multiplier)
        slot_symbol = SLOTS[slot_index]

        final_board_col = int(slot_index * (TOTAL_COLS - 1) / (len(SLOTS) - 1))

        await message.clear_reactions()

        embed.description = (
            f"risk: {risk}\n"
            f"bet: {amount}\n"
            f"wallet: {data[user_id]['wallet']} cores"
        )
        await message.edit(embed=embed)

        # simulate drop
        current_col = TOTAL_COLS // 2
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

        # animate
        for r in range(ROWS):
            board = build_board(path, path[r], r)
            embed.description = f"```\n{board}\n```"
            await message.edit(embed=embed)
            await asyncio.sleep(0.4)

        winnings = int(amount * multiplier)
        profit = winnings - amount

        data[user_id]["wallet"] -= amount
        data[user_id]["wallet"] += winnings
        save_bank(data)

        result_text = (
            f"bet: {amount}\n"
            f"multiplier: {multiplier}x\n"
            f"winnings: {winnings}\n"
            f"{'profit' if profit >= 0 else 'loss'}: {abs(profit)}"
        )

        # color by outcome
        if multiplier < 1:
            embed.color = 0xed4245
        elif multiplier == 1:
            embed.color = 0xfee75c
        else:
            embed.color = 0x57f287

        embed.description = f"```\n{build_board(path, path[-1], ROWS - 1)}\n```\n{result_text}"

        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Plinko(bot))