from decimal import ROUND_FLOOR, Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.views import CURRENT_DATE

from goals.models import Goals
from goals.forms import GoalAddForm, GoalEditForm
# Create your views here.

@login_required
def view_all_goals(request):
    all_goals = Goals.objects.all()

    return render(request, 'all_goals.html', {'date': CURRENT_DATE,
                                              'goals': all_goals})

@login_required
def view_goal(request, id):

    goal = Goals.objects.get(id=id)

    percent = Decimal(00.00)

    if request.method == "POST":
        form = GoalEditForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save(commit=False)
            if (goal.current_value != 0 ):
                percent = (goal.current_value / goal.goal_value) * 100
                percent = percent.quantize(Decimal("1.00"), ROUND_FLOOR)
            goal.current_percent = percent
            goal.save()
    else:
        form = GoalEditForm(instance=goal)

    return render(request, 'view_goal.html', {'date': CURRENT_DATE, 'form': form, 'goal': goal})

@login_required
def add_goal(request):
    if request.method == "POST":
        form = GoalAddForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.save()
    else:
        form = GoalAddForm()

    return render(request, 'add_goal.html', {'form': form, 'date': CURRENT_DATE})

@login_required
def delete_goal(request, id):
    goal = Goals.objects.get(id=id)
    goal.delete()
    return view_all_goals(request)