import discord
import requests
from discord.ext import commands


bot = commands.Bot(command_prefix='!',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')

with open("token.txt") as f:
    token = f.read()

@bot.command()
async def ping(ctx):
    ping_embed = discord.Embed(title="Pong", description="Latency in ms", color=discord.Color.random())
    ping_embed.add_field(name="Moderabot's Latency", value=f"{round(bot.latency * 1000)}ms",inline = False)
    ping_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
    await ctx.send(embed=ping_embed)

bot.run(token)