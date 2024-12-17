from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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
    violations = Violation.objects.select_related('user', 'rule')
    return render(request, 'violation_list.html', {'violations': violations})

def home(request):
    return render(request, 'home.html')
