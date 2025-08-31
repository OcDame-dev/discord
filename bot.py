import os
import requests
import discord
from discord.ext import commands

# Intents (required for new Discord API)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

def get_usd_to_gbp():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=GBP"
    response = requests.get(url).json()
    return response["rates"]["GBP"]

@bot.command()
async def getquote(ctx, product_cost: float, weight_per_unit: float, quantity: int, shipping_rate: float):
    try:
        # Fetch live exchange rate
        usd_to_gbp = get_usd_to_gbp()

        # USD calculations
        order_cost_usd = product_cost * quantity
        total_weight = weight_per_unit * quantity
        shipping_cost_usd = total_weight * shipping_rate
        landed_cost_usd = order_cost_usd + shipping_cost_usd

        # GBP conversions
        product_cost_gbp = product_cost * usd_to_gbp
        shipping_rate_gbp = shipping_rate * usd_to_gbp
        order_cost_gbp = order_cost_usd * usd_to_gbp
        shipping_cost_gbp = shipping_cost_usd * usd_to_gbp
        landed_cost_gbp = landed_cost_usd * usd_to_gbp

        # Build response
        message = (
            f"📦 **Product Cost (per unit):** ${product_cost:.2f} | £{product_cost_gbp:.2f}\n"
            f"🔢 **Quantity:** {quantity}\n"
            f"⚖️ **Weight per unit:** {weight_per_unit}kg\n"
            f"🚚 **Shipping rate:** ${shipping_rate:.2f}/kg | £{shipping_rate_gbp:.2f}/kg\n\n"
            f"💰 **Order Cost:** ${order_cost_usd:,.2f} | £{order_cost_gbp:,.2f}\n"
            f"⚖️ **Total Weight:** {total_weight}kg\n"
            f"🚛 **Total Shipping:** ${shipping_cost_usd:,.2f} | £{shipping_cost_gbp:,.2f}\n\n"
            f"✅ **Total Landed Cost:** ${landed_cost_usd:,.2f} | £{landed_cost_gbp:,.2f}\n"
            f"💱 **Exchange Rate:** 1 USD = {usd_to_gbp:.2f} GBP"
        )

        await ctx.send(message)

    except Exception as e:
        await ctx.send("⚠️ Usage: `/getquote <product_cost> <weight_per_unit> <quantity> <shipping_rate>`")

# Run bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
