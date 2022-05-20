from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Incomes
from .forms import IncomeEditForm, IncomeAddForm

from main.views import CURRENT_DATE, MONTH_NAMES


@login_required
def view_monthly_incomes(request, year, month):
    date = datetime(year, month, 1)

    if request.method == "POST":
        form = IncomeAddForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.date = date
            income.save()
    else:
        form = IncomeAddForm()

    incomes = Incomes.objects.filter(date=date)

    if len(incomes) == 0:
        Incomes.objects.create(date=date, name='Salary')
        incomes = [Incomes.objects.get(date=date)]

    return render(request, 'monthly_income.html',
                  {'date': CURRENT_DATE,
                   'cur_month': MONTH_NAMES[month],
                   'year': year,
                   'month': month,
                   'incomes': incomes,
                   'form': form})


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

    return render(request, 'income_edit.html',
                  {'date': CURRENT_DATE,
                   'income': income,
                   'form': form,
                   })


@login_required
def income_delete(request, id, year, month):
    income = Incomes.objects.get(id=id)
    income.delete()
    # return redirect('index')
    return view_monthly_incomes(request, year, month)
