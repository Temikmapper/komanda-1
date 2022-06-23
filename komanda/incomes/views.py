from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ConstantIncomes, AdditionalIncomes
from .forms import (
    ConstIncomeHistoryAddForm,
    IncomeEditForm,
    IncomeAddForm,
    ConstIncomeAddForm,
    ConstIncomeEditForm,
    BumpIncomeForm,
)

from main.views import MONTH_NAMES


@login_required
def view_monthly_incomes(request, year, month):

    incomes = AdditionalIncomes.get_objects_in_month(year, month)
    constant_incomes = ConstantIncomes.get_objects_in_month(year, month)

    return render(
        request,
        "monthly_income.html",
        {
            "cur_month": MONTH_NAMES[month],
            "year": year,
            "month": month,
            "incomes": incomes,
            "constant_incomes": constant_incomes,
        },
    )


@login_required
def income_edit(request, id, year, month):
    income = AdditionalIncomes.objects.get(id=id)

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
            "income": income,
            "form": form,
        },
    )


@login_required
def income_delete(request, id, year, month):
    income = AdditionalIncomes.objects.get(id=id)
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
            "form": form,
        },
    )


@login_required
def view_all_constant_incomes(request):
    current_incomes = ConstantIncomes.get_objects_in_month(
        date.today().year, date.today().month
    )
    outdated_incomes = ConstantIncomes.objects.filter(finish_date__lte=date.today())
    return render(
        request,
        "view_all_constant_incomes.html",
        {"incomes": current_incomes, "outdated_incomes": outdated_incomes},
    )


@login_required
def delete_constant_income(request, id):
    income = ConstantIncomes.objects.get(id=id)
    income.delete()

    return redirect("view_all_constant_incomes")


@login_required
def edit_constant_income(request, id):
    income = ConstantIncomes.objects.get(id=id)

    if request.method == "POST":
        form = ConstIncomeEditForm(request.POST, instance=income)
        if form.is_valid():
            income = form.save(commit=False)
            income.save()
            return redirect("view_all_constant_incomes")
    else:
        form = ConstIncomeEditForm(instance=income)

    return render(
        request,
        "edit_constant_income.html",
        {"form": form, "income": income},
    )


@login_required
def bump_constant_income(request, id):
    income = ConstantIncomes.objects.get(id=id)

    if income.finish_date < date.today():
        return redirect("view_all_constant_incomes")

    if request.method == "POST":
        form = BumpIncomeForm(request.POST)
        if form.is_valid():
            bump = form.save(commit=False)
            bump.income = income
            bump.save()
            return redirect("view_all_constant_incomes")
    else:
        form = BumpIncomeForm()

    return render(
        request,
        "bump_constant_income.html",
        {"form": form, "income": income},
    )


@login_required
def add_constant_income(request):

    if request.method == "POST":
        income_form = ConstIncomeAddForm(request.POST)
        value_form = ConstIncomeHistoryAddForm(request.POST)
        if income_form.is_valid() and value_form.is_valid():
            income = income_form.save(commit=False)
            value = value_form.save(commit=False)
            ConstantIncomes.objects.create(
                start_date=income.start_date, name=income.name, value=value.value
            )
            return redirect("view_all_constant_incomes")
    else:
        income_form = ConstIncomeAddForm()
        value_form = ConstIncomeHistoryAddForm()

    return render(
        request,
        "add_const_income.html",
        {"income_form": income_form, "income_value_form": value_form},
    )


@login_required
def view_constant_income(request, id):

    income = ConstantIncomes.objects.get(id=id)

    return render(
        request,
        "view_constant_income.html",
        {
            "income": income,
        },
    )
