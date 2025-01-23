from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

from .models import User, Rule, Violation

# View pentru a lista utilizatorii
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

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
    violations = Violation.objects.select_related('user_id', 'rule_id')
    return render(request, 'violation_list.html', {'violations': violations})

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

        # Creare regulă în baza de date
        Rule.objects.create(
            description=description,
            severity=int(severity),
            status=True,
            created_at=timezone.now(),
            lastUpdate=timezone.now()
        )
        return redirect('rule_list')

    return render(request, 'add_rule.html')

def rules_list(request):
    rules = Rule.objects.all()
    return render(request, 'moderabot/rules_list.html', {'rules': rules})

def edit_rule(request, rule_id):
    rule = get_object_or_404(Rule, rule_id=rule_id)
    
    if request.method == 'POST':
        # Update rule
        rule.description = request.POST.get('description')
        rule.severity = request.POST.get('severity')
        rule.status = request.POST.get('status') == 'on'
        rule.save()
        messages.success(request, 'Regula a fost actualizată cu succes!')
        return redirect('rules_list')
        
    return render(request, 'moderabot/edit_rule.html', {'rule': rule})

