from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from discord.ext import commands
import discord
from asgiref.sync import sync_to_async

from .models import User, Rule, Violation

# View pentru a lista utilizatorii
def user_list(request):
    users = User.objects.all().order_by('-severity_amount')
    return render(request, 'moderabot/user_list.html', {'users': users})

# View pentru a lista toate regulile în format JSON
def rule_list(request):
    rules = Rule.objects.all()
    return render(request, 'rule_list.html', {'rules': rules})

# View pentru a afișa o regulă după ID în format JSON
def rule_detail(request, rule_id):
    rule = get_object_or_404(Rule, pk=rule_id)
    return JsonResponse({
        "id": rule.id,
        "severity": rule.severity,
        "status": rule.status,
        "description": rule.description
    })

# View pentru a lista toate abaterile
def violation_list(request):
    violations = Violation.objects.select_related('user', 'rule').all().order_by('-timestamp')
    return render(request, 'moderabot/violation_list.html', {'violations': violations})

def home(request):
    return render(request, 'home.html')

# views.py
from django.shortcuts import render, redirect
from .models import Rule

# views.py
from django.shortcuts import render, redirect
from .models import Rule

def add_rule(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        severity = request.POST.get('severity')
        status = request.POST.get('status') == 'true'
        
        Rule.objects.create(
            description=description,
            severity=int(severity),
            status=status,
            created_at=timezone.now(),
            lastUpdate=timezone.now()
        )
        messages.success(request, 'Regula a fost adăugată cu succes!')
        return redirect('rules_list')
        
    return render(request, 'moderabot/add_rule.html')

def rules_list(request):
    rules = Rule.objects.all()
    return render(request, 'moderabot/rules_list.html', {'rules': rules})

def edit_rule(request, rule_id):
    rule = get_object_or_404(Rule, rule_id=rule_id)
    
    if request.method == 'POST':
        # Update rule
        rule.description = request.POST.get('description')
        rule.severity = request.POST.get('severity')
        rule.status = request.POST.get('status') == 'true'
        rule.save()
        messages.success(request, 'Regula a fost actualizată cu succes!')
        return redirect('rules_list')
        
    return render(request, 'moderabot/edit_rule.html', {'rule': rule})

def welcome(request):
    return render(request, 'moderabot/welcome.html')

def delete_rule(request, rule_id):
    rule = get_object_or_404(Rule, rule_id=rule_id)
    if request.method == 'POST':
        rule.delete()
        messages.success(request, 'Regula a fost ștearsă cu succes!')
        return redirect('rules_list')
    return redirect('rules_list')

async def mute_discord_user(user_id, guild_id):
    try:
        from Moderabot.disc.bot import bot
        guild = bot.get_guild(guild_id)
        if guild:
            member = await guild.fetch_member(user_id)
            if member:
                muted_role = discord.utils.get(guild.roles, name="Muted")
                if not muted_role:
                    # Creează rolul Muted dacă nu există
                    muted_role = await guild.create_role(name="Muted")
                    for channel in guild.channels:
                        await channel.set_permissions(muted_role, speak=False, send_messages=False)
                await member.add_roles(muted_role)
                return True
    except Exception as e:
        print(f"Eroare la mutarea utilizatorului: {e}")
    return False

def reset_severity(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, user_id=user_id)
        user.severity_amount = 0
        user.save()
        messages.success(request, f'Punctele de severitate pentru {user.username} au fost resetate.')
    return redirect('user_list')

def mute_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, user_id=user_id)
        # Înlocuiește cu ID-ul serverului tău Discord
        GUILD_ID = 123456789  # Trebuie să pui ID-ul corect al serverului tău
        
        import asyncio
        success = asyncio.run(mute_discord_user(user_id, GUILD_ID))
        
        if success:
            messages.success(request, f'Utilizatorul {user.username} a fost mutat pe Discord.')
        else:
            messages.error(request, f'Nu s-a putut muta utilizatorul {user.username}.')
    return redirect('user_list')

