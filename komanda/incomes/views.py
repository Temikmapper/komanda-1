from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ConstantIncomes, AdditionalIncomes
from .forms import (
    ConstantIncomeAddForm,
    IncomeEditForm,
    IncomeAddForm,
    ConstantIncomeEditForm,
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
    """Страница изменения разового дохода
    """

    income = AdditionalIncomes.objects.get(id=id)

    if request.method == "POST":
        form = IncomeEditForm(request.POST, instance=income)
        if form.is_valid():
            income = form.save(commit=False)
            income.save()
    else:
        form = IncomeEditForm(instance=income)

    return render(
        request,
        "income_edit.html",
        {
            "instance": income,
            "form": form,
        },
    )


@login_required
def income_delete(request, id, year, month):
    income = AdditionalIncomes.objects.get(id=id)
    income.delete()
    return view_monthly_incomes(request, year, month)


@login_required
def add_income(request, year, month):
    date = datetime(year, month, 1)

    if request.method == "POST":
        form = IncomeAddForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.date = date
            income.save()

            return redirect("view_monthly_incomes", year, month)
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
        form = ConstantIncomeEditForm(request.POST, instance=income)
        if form.is_valid():
            income = form.save(commit=False)
            income.save()
            return redirect("view_all_constant_incomes")
    else:
        form = ConstantIncomeEditForm(instance=income)

    return render(
        request,
        "edit_constant_income.html",
        {"form": form, "instance": income},
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
        {"form": form, "instance": income},
    )


@login_required
def add_constant_income(request):
    """Страница добавления постоянного дохода"""

    if request.method == "POST":
        form = ConstantIncomeAddForm(request.POST)
        if form.is_valid():
            income = form.cleaned_data
            ConstantIncomes.objects.create(
                start_date=income["start_date"],
                name=income["name"],
                value=income["value"],
            )
            return redirect("view_all_constant_incomes")
    else:
        form = ConstantIncomeAddForm()

    return render(
        request,
        "add_constant_income.html",
        {"form": form},
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
