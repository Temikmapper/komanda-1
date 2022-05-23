from datetime import datetime
from decimal import ROUND_FLOOR, Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.views import CURRENT_DATE

from goals.models import Goals, GoalStatus
from goals.forms import GoalAddForm, GoalStatusAddForm
# Create your views here.


@login_required
def view_all_goals(request):
    all_goals = Goals.objects.all()

    goals_statuses = {}

    for goal in all_goals:
        goal_statuses = GoalStatus.objects.filter(goal=goal)
        latest_status = goal_statuses.latest('date')
        goals_statuses[goal] = latest_status

    return render(request, 'all_goals.html', {'date': CURRENT_DATE,
                                              'goals': all_goals,
                                              'goals_statuses': goals_statuses})


@login_required
def view_goal(request, id):

    goal = Goals.objects.get(id=id)

    percent = Decimal(00.00)

    if request.method == "POST":
        form = GoalStatusAddForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.goal = goal
            if (status.value != 0 ):
                percent = (status.value / goal.value) * 100
                percent = percent.quantize(Decimal("1.00"), ROUND_FLOOR)
            status.percent = percent
            status.save()
    else:
        form = GoalStatusAddForm()

    goal_statuses = GoalStatus.objects.filter(goal=goal)
    latest_status = goal_statuses.latest('date')

    return render(request, 'view_goal.html', {'date': CURRENT_DATE,
                                              'form': form,
                                              'goal': goal,
                                              'goal_statuses': goal_statuses,
                                              'latest_status': latest_status})


@login_required
def add_goal(request):
    if request.method == "POST":
        form = GoalAddForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.save()
            GoalStatus.objects.create(date = datetime.today(), value = Decimal(0.0), goal = goal)
            return view_all_goals(request)
    else:
        form = GoalAddForm()


    return render(request, 'add_goal.html', {'form': form, 'date': CURRENT_DATE})


@login_required
def delete_goal(request, id):
    goal = Goals.objects.get(id=id)
    goal.delete()
    return view_all_goals(request)
