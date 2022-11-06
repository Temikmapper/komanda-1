from calendar import monthrange
from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from incomes.views import AdditionalIncomes, ConstantIncomes
from expenses.views import ConstantExpenses
from goals.models import Goals
from piggy.models import Piggies
from main.views import MONTH_NAMES, MONTHES

# Create your views here.


@login_required
def view_resume(request, year, month):
    """Представление сводки месяца"""

    last_day = monthrange(year, month)[1]

    global START_OF_MONTH
    global END_OF_MONTH

    START_OF_MONTH = datetime(year, month, 1)
    END_OF_MONTH = datetime(year, month, last_day)

    constant_incomes = ConstantIncomes.get_objects_in_month(year, month)
    additional_incomes = AdditionalIncomes.get_objects_in_month(year, month)
    all_incomes = list(constant_incomes) + list(additional_incomes)
    incomes = {}
    for income in all_incomes:
        incomes.update({income.name: income.get_value_in_month(year, month)})
    total_income = ConstantIncomes.get_sum_in_month(
        year, month
    ) + AdditionalIncomes.get_sum_in_month(year, month)

    constant_expenses = ConstantExpenses.get_objects_in_month(year, month)
    total_expense = ConstantExpenses.get_sum_in_month(year, month)

    goals = Goals.objects.all()

    piggy_capital = {}
    piggies = Piggies.objects.all()
    for piggy in piggies:
        piggy_capital[piggy] = piggy.get_capital_till_date(END_OF_MONTH)

    return render(
        request,
        "resume.html",
        {
            "year": year,
            "month": month,
            "monthes": MONTHES,
            "cur_month": MONTH_NAMES[month],
            "incomes": incomes,
            "total_income": total_income,
            "expenses": constant_expenses,
            "total_expense": total_expense,
            "goals": goals,
            "piggies": piggy_capital,
        },
    )
