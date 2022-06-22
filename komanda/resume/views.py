from calendar import monthrange
from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from incomes.views import get_constant_incomes, get_additional_incomes
from expenses.views import get_constant_expenses
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

    constant_incomes = get_constant_incomes(START_OF_MONTH, END_OF_MONTH)
    additional_incomes = get_additional_incomes(START_OF_MONTH)
    all_incomes = constant_incomes | additional_incomes
    total_income = sum(all_incomes.values())

    constant_expenses = get_constant_expenses(START_OF_MONTH, END_OF_MONTH)
    total_expense = sum(constant_expenses.values())

    # goals = get_last_goals_statuses(START_OF_MONTH, END_OF_MONTH)

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
            "incomes": all_incomes,
            "total_income": total_income,
            "expenses": constant_expenses,
            "total_expense": total_expense,
            # "goals": goals,
            "piggies": piggy_capital,
        },
    )
