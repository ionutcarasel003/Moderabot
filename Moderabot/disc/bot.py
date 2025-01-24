import discord
from asgiref.sync import sync_to_async
from discord.ext import commands
from discord import app_commands
import os

from Moderabot.models import Rule, User

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
API_BASE_URL = "http://localhost:8000/"

bot_instance = bot  # Adaugă această linie pentru a expune instanța botului

@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.load_extension('Moderabot.disc.message_monitoring')

@bot.command()
async def ping(ctx):
    ping_embed = discord.Embed(title="Pong", description="Latency in ms", color=discord.Color.random())
    ping_embed.add_field(name="Moderabot's Latency", value=f"{round(bot.latency * 1000)}ms",inline = False)
    ping_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
    await ctx.send(embed=ping_embed)

@bot.command()
async def edit(ctx):
    if ctx.author.guild_permissions.administrator:
        try:
            await ctx.author.send(f"Accesează {API_BASE_URL} pentru a edita regulile.")
            await ctx.send("Mesajul tău privat a fost trimis!")
        except discord.Forbidden:
            await ctx.send("Nu pot trimite un mesaj privat. Verifică setările tale de DM.")
    else:
        await ctx.send("Această comandă este disponibilă doar pentru administratori.")

@bot.command()
async def rules(ctx):
    """Afișează toate regulile active"""
    try:
        get_rules = sync_to_async(lambda: list(Rule.objects.filter(status=True)))
        rules = await get_rules()
        
        if not rules:
            await ctx.send("Nu există reguli active momentan.")
            return
            
        embed = discord.Embed(title="Cuvinte nepermise", color=discord.Color.blue())
        for rule in rules:
            embed.add_field(
                name=f" (Severitate: {rule.severity})",
                value=rule.description, 
                inline=False
            )
        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Eroare la afișarea regulilor: {e}")
        await ctx.send("A apărut o eroare la afișarea regulilor.")

@bot.command()
async def status(ctx):
    """Afișează statusul userului"""
    try:
        get_user = sync_to_async(User.objects.get)
        user = await get_user(user_id=ctx.author.id)
        embed = discord.Embed(title="Statusul Tău", color=discord.Color.green())
        embed.add_field(name="Puncte de severitate", value=user.severity_amount)
        embed.add_field(name="Status", value="Activ" if user.status else "Inactiv")
        await ctx.send(embed=embed)
    except User.DoesNotExist:
        await ctx.send("Nu ai nicio încălcare înregistrată!")







async def run_discord_bot():
    try:
        with open("token.txt") as f:
            token = f.read().strip()
        print("Token găsit cu succes!")
        await bot.start(token)
        
    except FileNotFoundError:
        print("Error: Nu am găsit fișierul 'token.txt'.")
        return

