from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.views import CURRENT_DATE

from goals.models import Goals
from goals.forms import GoalAddForm, GoalBumpForm, GoalEditForm

# Create your views here.


@login_required
def view_all_goals(request):
    all_goals = Goals.objects.all()

    return render(
        request,
        "all_goals.html",
        {"date": CURRENT_DATE, "goals": all_goals},
    )


@login_required
def bump_goal(request, id):
    goal = Goals.objects.get(id=id)

    if request.method == "POST":
        form = GoalBumpForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            goal.bump(date=data.date, value=data.value)
            return redirect("view_all_goals")
    else:
        form = GoalBumpForm()

    return render(
        request,
        "bump_goal.html",
        {
            "date": CURRENT_DATE,
            "form": form,
            "goal": goal,
        },
    )


@login_required
def edit_goal(request, id):
    goal = Goals.objects.get(id=id)

    if request.method == "POST":
        form = GoalEditForm(request.POST, instance=goal)
        if form.is_valid():
            edited_goal = form.save(commit=False)
            edited_goal.save()
            return redirect(goal.get_absolute_url())
    else:
        form = GoalEditForm(instance=goal)

    return render(
        request,
        "edit_goal.html",
        {
            "date": CURRENT_DATE,
            "form": form,
            "goal": goal,
        },
    )


@login_required
def view_goal(request, id):
    goal = Goals.objects.get(id=id)

    return render(
        request,
        "view_goal.html",
        {
            "date": CURRENT_DATE,
            "goal": goal,
        },
    )


@login_required
def add_goal(request):
    if request.method == "POST":
        form = GoalAddForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.save()
            return redirect("view_all_goals")
    else:
        form = GoalAddForm()

    return render(request, "add_goal.html", {"form": form, "date": CURRENT_DATE})


@login_required
def delete_goal(request, id):
    goal = Goals.objects.get(id=id)
    goal.delete()
    return view_all_goals(request)
