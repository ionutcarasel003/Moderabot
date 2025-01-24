from discord.ext import commands
from django.utils import timezone
import discord
from discord import app_commands
from asgiref.sync import sync_to_async
from Moderabot.models import Rule, User, Violation

class MessageMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
            
        if message.content.startswith('!'):
            return
            
        try:
            # Verificăm dacă utilizatorul are roluri de moderare
            is_staff = message.author.guild_permissions.administrator or \
                      any(role.permissions.kick_members or 
                          role.permissions.ban_members or 
                          role.permissions.manage_messages 
                          for role in message.author.roles)
            
            
            # Convertim query-urile în async
            get_rules = sync_to_async(lambda: list(Rule.objects.filter(status=True)))
            get_or_create_user = sync_to_async(User.objects.get_or_create)
            create_violation = sync_to_async(Violation.objects.create)
            
            # Obținem toate regulile active
            rules = await get_rules()
            
            # Convertim mesajul la lowercase pentru comparare
            message_content = message.content.lower()
            
            # Verificăm fiecare regulă
            for rule in rules:
                # Verificăm dacă cuvântul nepermis este conținut în mesaj
                if rule.description.lower() in message_content.split():
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
                        created_at=timezone.now()
                    )
                    
                    # Incrementăm severity_amount pentru user
                    user.severity_amount += rule.severity
                    await sync_to_async(user.save)()

                    # Verificăm pentru ban doar dacă nu e staff
                    if user.severity_amount > 10:
                        try:
                            await message.author.ban(reason=f"Severity amount peste 10 ({user.severity_amount})")
                            await message.channel.send(f"Utilizatorul {message.author.mention} a fost banat pentru că a acumulat prea multe puncte de severitate ({user.severity_amount}).")
                        except discord.Forbidden:
                            await message.channel.send("Nu am permisiunea să banez acest utilizator.")
                        except Exception as e:
                            print(f"Eroare la banare: {e}")
                    
                    # Trimitem avertisment
                    embed = discord.Embed(
                        title="⚠️ Avertisment",
                        description=f"Mesajul tău {user.username} a fost șters pentru că are în conținut limbaj dezagreabil: {rule.description}",
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

    @app_commands.command(name = 'kick', description = 'Kicks a specified member.')
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.kick(member)
        await interaction.response.send_message(f"Kicked {member.mention}.",ephemeral=True)

    @app_commands.command(name='ban', description='Bans a specified member.')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.ban(member)
        await interaction.response.send_message(f"Banned {member.mention}.", ephemeral=True)



    @commands.command()
    async def unban(self, ctx, *, member):
        try:
            # Convertim input-ul în format ID sau username#discriminator
            try:
                # Încercăm să extragem ID-ul din mențiune sau ID direct
                member_id = int(member.strip('<@!>'))
                banned_users = [entry async for entry in ctx.guild.bans()]
                banned_user = discord.utils.get(banned_users, user__id=member_id)
            except ValueError:
                # Dacă nu e ID, căutăm după username
                banned_users = [entry async for entry in ctx.guild.bans()]
                banned_user = discord.utils.get(banned_users, user__name=member)

            if banned_user is None:
                await ctx.send(f"Nu am găsit utilizatorul {member} în lista de banuri.")
                return

            # Verificăm dacă persoana care execută comanda are permisiuni
            if not ctx.author.guild_permissions.ban_members:
                await ctx.send("Nu ai permisiunea să debanezi utilizatori!")
                return

            await ctx.guild.unban(banned_user.user)
            
            # Resetăm severity_amount pentru utilizator în baza de date
            get_user = sync_to_async(User.objects.get)
            try:
                user = await get_user(user_id=banned_user.user.id)
                user.severity_amount = 0
                await sync_to_async(user.save)()
            except User.DoesNotExist:
                pass  # Ignorăm dacă utilizatorul nu există în baza noastră de date

            embed = discord.Embed(
                title="✅ Unban Reușit",
                description=f"Utilizatorul {banned_user.user.name} a fost debanat.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("Nu am permisiunea să debanez utilizatori!")
        except Exception as e:
            await ctx.send(f"A apărut o eroare la debanare: {str(e)}")
            print(f"Eroare la debanare: {e}")

async def setup(bot):
    await bot.add_cog(MessageMonitor(bot))
