from discord.ext import commands
from django.utils import timezone
import discord
from asgiref.sync import sync_to_async
from Moderabot.models import Rule, User, Violation

class MessageMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignoră mesajele de la bot
        if message.author == self.bot.user:
            return
            
        # Ignoră comenzile
        if message.content.startswith('!'):
            return
            
        try:
            # Convertim query-urile în async
            get_rules = sync_to_async(lambda: list(Rule.objects.filter(status=True)))
            get_or_create_user = sync_to_async(User.objects.get_or_create)
            create_violation = sync_to_async(Violation.objects.create)
            
            # Obținem toate regulile active
            rules = await get_rules()
            
            # Verificăm fiecare regulă
            for rule in rules:
                if rule.description.lower() in message.content.lower():
                    # Creăm sau obținem userul
                    user, created = await get_or_create_user(
                        user_id=message.author.id,
                        defaults={
                            'username': str(message.author),
                            'severity_amount': 0,
                            'status': True
                        }
                    )
                    
                    # Înregistrăm violarea
                    await create_violation(
                        user_id=user.user_id,
                        rule_id=rule.rule_id,
                        timestamp=timezone.now()
                    )
                    
                    # Incrementăm severity_amount pentru user
                    user.severity_amount += rule.severity
                    await sync_to_async(user.save)()
                    
                    # Trimitem avertisment
                    embed = discord.Embed(
                        title="⚠️ Avertisment",
                        description=f"Mesajul tău a fost șters pentru că încalcă regula: {rule.description}",
                        color=discord.Color.red()
                    )
                    embed.add_field(name="Severitate", value=f"+{rule.severity} puncte")
                    embed.add_field(name="Total puncte", value=f"{user.severity_amount}")
                    await message.channel.send(embed=embed)
                    
                    # Ștergem mesajul
                    await message.delete()
                    break
                    
        except Exception as e:
            print(f"Eroare în timpul procesării mesajului: {e}")
            import traceback
            traceback.print_exc()

async def setup(bot):
    await bot.add_cog(MessageMonitor(bot))
