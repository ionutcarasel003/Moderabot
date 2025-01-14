from django.utils import timezone
import discord
from asgiref.sync import sync_to_async
from Moderabot.models import Rule, User, Violation

class MessageMonitor:
    async def check_message(self, message):
        try:
            # Convertim query-urile sincrone în asincrone
            get_rules = sync_to_async(Rule.objects.filter)
            get_or_create_user = sync_to_async(User.objects.get_or_create)
            create_violation = sync_to_async(Violation.objects.create)
            
            # Obținem regulile active
            rules = await get_rules(status=True)
            
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
                    
                    # Creăm violația
                    await create_violation(
                        user_id=user.user_id,
                        rule_id=rule.rule_id,
                        timestamp=timezone.now()
                    )
                    
                    # Actualizăm severity_amount
                    user.severity_amount += rule.severity
                    await sync_to_async(user.save)()
                    
                    # Trimitem avertismentul
                    embed = discord.Embed(
                        title="⚠️ Avertisment",
                        description=f"Ai încălcat regula: {rule.description}",
                        color=discord.Color.red()
                    )
                    embed.add_field(name="Severitate", value=f"{rule.severity} puncte")
                    embed.add_field(name="Total puncte", value=f"{user.severity_amount}")
                    await message.channel.send(embed=embed)
                    
                    if rule.severity >= 5:
                        await message.delete()
                        
        except Exception as e:
            print(f"Eroare în timpul procesării mesajului: {e}")
