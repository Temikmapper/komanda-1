from calendar import monthrange
from datetime import datetime, timedelta
from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ConstantIncomeHistory, ConstantIncomes, Incomes
from .forms import (
    IncomeEditForm,
    IncomeAddForm,
    ConstantIncomeAddForm,
    ConstantIncomeFinishForm,
    IncomeEditForm,
)

from main.views import CURRENT_DATE, MONTH_NAMES


@login_required
def view_monthly_incomes(request, year, month):
    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    incomes = Incomes.objects.filter(date=start_of_month)

    constant_incomes = get_constant_incomes(start_of_month, end_of_month)

    return render(
        request,
        "monthly_income.html",
        {
            "date": CURRENT_DATE,
            "cur_month": MONTH_NAMES[month],
            "year": year,
            "month": month,
            "incomes": incomes,
            "constant_incomes": constant_incomes,
        },
    )


@login_required
def income_edit(request, id, year, month):
    income = Incomes.objects.get(id=id)

    if request.method == "POST":
        form = IncomeEditForm(request.POST, instance=income)
        if form.is_valid():
            income = form.save(commit=False)
            income.name
            income.save()
    else:
        form = IncomeEditForm(instance=income)

    return render(
        request,
        "income_edit.html",
        {
            "date": CURRENT_DATE,
            "income": income,
            "form": form,
        },
    )


@login_required
def income_delete(request, id, year, month):
    income = Incomes.objects.get(id=id)
    income.delete()
    return view_monthly_incomes(request, year, month)


@login_required
def income_add(request, year, month):

    date = datetime(year, month, 1)

    if request.method == "POST":
        form = IncomeAddForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.date = date
            income.save()
    else:
        form = IncomeAddForm()

    return render(
        request,
        "add_income.html",
        {
            "date": CURRENT_DATE,
            "form": form,
        },
    )


def view_all_constant_incomes(request):
    all_incomes = ConstantIncomes.objects.all()
    return render(
        request,
        "view_all_constant_incomes.html",
        {"date": CURRENT_DATE, "incomes": all_incomes},
    )


def delete_constant_income(request, id):
    income = ConstantIncomes.objects.get(id=id)
    income.delete()

    return view_all_constant_incomes(request)


def add_constant_income(request):

    if request.method == "POST":
        income_form = ConstantIncomeAddForm(request.POST)
        value_form = IncomeEditForm(request.POST)
        if income_form.is_valid() and value_form.is_valid():
            income = income_form.save(commit=False)
            income.finish_date = income.start_date + timedelta(760)
            income.save()
            value = value_form.save(commit=False)
            income = ConstantIncomes.objects.get(id=income.id)
            value.date = income.start_date
            value.income = income
            value.save()
    else:
        income_form = ConstantIncomeAddForm()
        value_form = IncomeEditForm()

    return render(
        request,
        "add_const_income.html",
        {"date": CURRENT_DATE, "income_form": income_form, "value_form": value_form},
    )


def view_constant_income(request, id):

    income = ConstantIncomes.objects.get(id=id)
    income_history = ConstantIncomeHistory.objects.filter(income=income)

    form = None

    if request.method == "POST":
        form = IncomeEditForm(request.POST)
        finish_form = ConstantIncomeFinishForm(request.POST, instance=income)
        if form.is_valid() and finish_form.is_valid():
            finish = finish_form.save(commit=False)
            finish.save()
            value = form.save(commit=False)
            value.date = datetime.today()
            value.income = income
            value.save()
    else:
        form = IncomeEditForm()
        finish_form = ConstantIncomeFinishForm(instance=income)

    return render(
        request,
        "view_constant_income.html",
        {
            "date": CURRENT_DATE,
            "income": income,
            "history": income_history,
            "form": form,
            "finish_form": finish_form,
        },
    )


def get_constant_incomes(start_of_month, end_of_month):

    actual_incomes = ConstantIncomes.objects.filter(
        start_date__lte=start_of_month
    ).filter(finish_date__gte=end_of_month)

    income_value = {}
    for income in actual_incomes:
        current_value = (
            ConstantIncomeHistory.objects.filter(income=income)
            .filter(date__lte=end_of_month)
            .last()
            .value
        )
        income_value[income] = current_value

    return income_value


def get_sum_constant_incomes(start_of_month, end_of_month):
    incomes = get_constant_incomes(start_of_month, end_of_month)

    return sum(incomes.values())


def get_additional_incomes(start_of_month):

    incomes = Incomes.objects.filter(date=start_of_month)

    income_value = {}
    for income in incomes:
        income_value[income] = income.value

    return income_value
