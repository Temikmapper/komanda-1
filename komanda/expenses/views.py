from calendar import monthrange
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from main.views import CURRENT_DATE, MONTH_NAMES

from expenses.models import (
    ConstantExpenses,
    ConstantExpenseHistory,
    UsualExpenses,
    Categories,
)
from expenses.forms import (
    UsualExpenseAddForm,
    CategoryAddForm,
    ConstantExpenseAddForm,
    ConstantExpenseFinishForm,
    ConstantExpenseEditForm,
)


@login_required
def view_all_expenses(request):
    data = UsualExpenses.objects.all()
    return render(request, "all_expenses.html", {"days": data, "date": CURRENT_DATE})


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
        {"form": form, "categories": categories, "date": CURRENT_DATE},
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

    today = date.today()
    categories = Categories.objects.all()
    recent_expenses = UsualExpenses.objects.all()[:10]

    return render(
        request,
        "add_usual_expense.html",
        {
            "expense_form": expense_form,
            "category_form": category_form,
            "date": CURRENT_DATE,
            "today": today,
            "categories": categories,
            "recent_expenses": recent_expenses
        },
    )


def add_constant_expense(request):

    if request.method == "POST":
        expense_form = ConstantExpenseAddForm(request.POST)
        value_form = ConstantExpenseEditForm(request.POST)
        if expense_form.is_valid() and value_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.finish_date = expense.start_date + timedelta(760)
            expense.save()
            value = value_form.save(commit=False)
            expense = ConstantExpenses.objects.get(id=expense.id)
            value.date = expense.start_date
            value.expense = expense
            value.save()
    else:
        expense_form = ConstantExpenseAddForm()
        value_form = ConstantExpenseEditForm()

    return render(
        request,
        "add_const_expense.html",
        {"date": CURRENT_DATE, "expense_form": expense_form, "value_form": value_form},
    )


def view_constant_expense(request, id):

    expense = ConstantExpenses.objects.get(id=id)

    if request.method == "POST":
        form = ConstantExpenseEditForm(request.POST)
        finish_form = ConstantExpenseFinishForm(request.POST, instance=expense)
        if form.is_valid() and finish_form.is_valid():
            finish = finish_form.save(commit=False)
            finish.save()
            value = form.save(commit=False)
            value.date = datetime.today()
            value.expense = expense
            value.save()
    else:
        form = ConstantExpenseEditForm()
        finish_form = ConstantExpenseFinishForm(instance=expense)

    return render(
        request,
        "view_constant_expense.html",
        {
            "date": CURRENT_DATE,
            "expense": expense,
            "form": form,
            "finish_form": finish_form,
        },
    )


def view_all_constant_expenses(request):

    all_expenses = ConstantExpenses.objects.all()

    return render(
        request,
        "view_all_constant_expenses.html",
        {"date": CURRENT_DATE, "expenses": all_expenses},
    )


def delete_constant_expense(request, id):
    expense = ConstantExpenses.objects.get(id=id)
    expense.delete()

    return view_all_constant_expenses(request)


def view_monthly_expenses(request, year, month):
    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    constant_expenses = get_constant_expenses(start_of_month, end_of_month)

    return render(
        request,
        "monthly_expenses.html",
        {
            "date": CURRENT_DATE,
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
    return redirect("/")


def get_constant_expenses(start_of_month, end_of_month):

    actual_expenses = ConstantExpenses.objects.filter(
        start_date__lte=start_of_month
    ).filter(finish_date__gte=end_of_month)

    expense_value = {}
    for expense in actual_expenses:
        value = (
            ConstantExpenseHistory.objects.filter(expense=expense)
            .filter(date__lte=end_of_month)
            .last()
            .value
        )
        expense_value[expense] = value

    return expense_value


def get_sum_constant_expenses(start_of_month, end_of_month):

    expenses = get_constant_expenses(start_of_month, end_of_month)

    total_expenses = sum(expenses.values())

    return total_expenses
