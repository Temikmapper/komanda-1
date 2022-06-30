from calendar import monthrange
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from expenses.models import ConstantExpenseHistoryItem
from main.views import MONTH_NAMES

from expenses.models import (
    ConstantExpenses,
    UsualExpenses,
    Categories,
)
from expenses.forms import (
    UsualExpenseAddForm,
    CategoryAddForm,
    ConstExpenseAddForm,
    ConstExpenseEditForm,
    ConstExpenseHistoryAddForm,
    BumpExpenseForm,
)


@login_required
def view_all_expenses(request):
    data = UsualExpenses.objects.all()
    return render(request, "all_expenses.html", {"days": data})


@login_required
def view_add_categories(request):
    categories = Categories.objects.all()
    if request.method == "POST":
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
    else:
        form = CategoryAddForm()

    return render(
        request,
        "categories.html",
        {"form": form, "categories": categories},
    )


@login_required
def delete_category(request, id):
    category = Categories.objects.get(id=id)
    category.delete()
    return redirect("view_add_categories")


@login_required
def add_usual_expense(request):
    if request.method == "POST":
        expense_form = UsualExpenseAddForm(request.POST)
        category_form = CategoryAddForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.save()
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.save()
    else:
        expense_form = UsualExpenseAddForm()
        category_form = CategoryAddForm()

    categories = Categories.objects.all()
    recent_expenses = UsualExpenses.objects.all()[:10]

    return render(
        request,
        "add_usual_expense.html",
        {
            "expense_form": expense_form,
            "category_form": category_form,
            "categories": categories,
            "recent_expenses": recent_expenses,
        },
    )


@login_required
def add_constant_expense(request):

    if request.method == "POST":
        expense_form = ConstExpenseAddForm(request.POST)
        value_form = ConstExpenseHistoryAddForm(request.POST)
        if expense_form.is_valid() and value_form.is_valid():
            expense = expense_form.save(commit=False)
            value = value_form.save(commit=False)
            ConstantExpenses.objects.create(
                start_date=expense.start_date, name=expense.name, value=value.value
            )
            return redirect("view_all_constant_expenses")
    else:
        expense_form = ConstExpenseAddForm()
        value_form = ConstExpenseHistoryAddForm()

    return render(
        request,
        "add_const_expense.html",
        {"expense_form": expense_form, "expense_value_form": value_form},
    )


@login_required
def view_constant_expense(request, id):

    expense = ConstantExpenses.objects.get(id=id)

    return render(
        request,
        "view_constant_expense.html",
        {"expense": expense},
    )


@login_required
def view_all_constant_expenses(request):

    current_expenses = ConstantExpenses.get_objects_in_month(
        date.today().year, date.today().month)
    outdated_expenses = ConstantExpenses.objects.filter(
        finish_date__lte=date.today())

    return render(
        request,
        "view_all_constant_expenses.html",
        {"expenses": current_expenses, "outdated_expenses": outdated_expenses},
    )


@login_required
def delete_constant_expense(request, id):
    expense = ConstantExpenses.objects.get(id=id)
    expense.delete()

    return redirect("view_all_constant_expenses")


@login_required
def edit_constant_expense(request, id):
    expense = ConstantExpenses.objects.get(id=id)

    if request.method == "POST":
        form = ConstExpenseEditForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.save()
            return redirect("view_all_constant_expenses")
    else:
        form = ConstExpenseEditForm(instance=expense)

    return render(
        request,
        "edit_constant_expense.html",
        {"form": form, "expense": expense},
    )


@login_required
def bump_constant_expense(request, id):
    expense = ConstantExpenses.objects.get(id=id)

    if expense.finish_date < date.today():
        return redirect("view_all_constant_expenses")

    if request.method == "POST":
        form = BumpExpenseForm(request.POST)
        if form.is_valid():
            bump = form.save(commit=False)
            bump.expense = expense
            bump.save()
            return redirect("view_all_constant_expenses")
    else:
        form = BumpExpenseForm()

    return render(
        request,
        "bump_constant_expense.html",
        {"form": form, "expense": expense},
    )


def view_monthly_expenses(request, year, month):

    constant_expenses = ConstantExpenses.get_objects_in_month(year, month)

    return render(
        request,
        "monthly_expenses.html",
        {
            "cur_month": MONTH_NAMES[month],
            "year": year,
            "month": month,
            "constant_expenses": constant_expenses,
        },
    )


@login_required
def delete_expense(request, id):
    expense = UsualExpenses.objects.get(id=id)
    expense.delete()
    return redirect("redirect_to_view_month")


@login_required
def chart(request, id):
    expense = ConstantExpenses.objects.get(id=id)
    objects = ConstantExpenseHistoryItem.objects.filter(expense=expense)
    data = []

    min_ = ConstantExpenseHistoryItem.objects.filter(expense=expense).first().date - timedelta(1)
    max_ = ConstantExpenseHistoryItem.objects.filter(expense=expense).last().date + timedelta(1)

    iteratior_min = date(min_.year, min_.month, 1)

    while (iteratior_min < max_):
        days = monthrange(iteratior_min.year, iteratior_min.month)[1]
        try:
            value = ConstantExpenseHistoryItem.objects.filter(expense=expense).filter(date__lte=iteratior_min).last().value
        except AttributeError:
            value = None
        label_value = {'x': iteratior_min,
                       'y': value}
        data.append(label_value)
        iteratior_min += timedelta(days)

    for object in objects:
        label_value = {'x': object.date,
                       'y': object.value}
        data.append(label_value)

    data = sorted(data, key=lambda student: student['x'])

    return JsonResponse(
        data={
            "data": data,
            "min": min_,
            "max": max_
        },
        status=200,
    )
