from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from goals.models import GoalBump, GoalExpense, Goals
from goals.forms import GoalAddForm, GoalAddExpenseForm, GoalEditForm, GoalBumpForm

# Create your views here.


@login_required
def view_all_goals(request):
    today = date.today()
    current_goals = Goals.objects.filter(finish_date__gte=today)
    outdated_expenses = Goals.objects.filter(finish_date__lt=today)

    return render(
        request,
        "all_goals.html",
        {
            "instances_color": "is-info",
            "instances": current_goals,
            "outdated_instances": outdated_expenses,
        },
    )


@login_required
def add_expense_goal(request, id):
    goal = Goals.objects.get(id=id)

    if request.method == "POST":
        form = GoalAddExpenseForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            goal.add_expense(date=data.date, value=data.value)
            return redirect("view_all_goals")
    else:
        form = GoalAddExpenseForm()

    return render(
        request,
        "expense_goal.html",
        {
            "form": form,
            "instance": goal,
        },
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
            "form": form,
            "instance": goal,
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
            "form": form,
            "instance": goal,
        },
    )


@login_required
def view_goal(request, id):
    goal = Goals.objects.get(id=id)

    return render(
        request,
        "view_goal.html",
        {
            "instance": goal,
            "instance_color": "is-info",
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

    return render(request, "add_goal.html", {"form": form})


@login_required
def delete_goal(request, id):
    goal = Goals.objects.get(id=id)
    goal.delete()
    return view_all_goals(request)

@login_required
def delete_goal_expense(request, goal_id: int, goal_expense_id: int):
    """Удалить трату цели.

    Args:
        goal_id (int): ID цели
        goal_expense_id (int): ID траты цели
    """
    goal = Goals.objects.only('id').get(id=goal_id)
    GoalExpense.objects.get(id=goal_expense_id).delete()

    return redirect(goal)


