from calendar import monthrange
from datetime import date, datetime, timedelta
from decimal import ROUND_FLOOR, Decimal

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from main.views import MONTH_NAMES, MONTHES
from expenses.models import UsualExpenses, ConstantExpenses
from incomes.models import AdditionalIncomes, ConstantIncomes


@login_required
def redirect_to_view_month(request):
    return redirect("view_month", date.today().year, date.today().month)


@login_required
def view_month(request, year, month):
    """Представление страницы месяца с актуальной для него информацией"""

    last_day = monthrange(year, month)[1]

    global START_OF_MONTH
    global END_OF_MONTH

    START_OF_MONTH = datetime(year, month, 1)
    END_OF_MONTH = datetime(year, month, last_day)

    daily_income = get_daily_income().quantize(Decimal("1.00"), ROUND_FLOOR)
    sum_of_usual_expenses = UsualExpenses.get_sum_in_month(year, month)
    sum_of_all_incomes = ConstantIncomes.get_sum_in_month(
        year, month
    ) + AdditionalIncomes.get_sum_in_month(year, month)
    sum_of_constant_expenses = ConstantExpenses.get_sum_in_month(year, month)
    data = get_balance_for_monthly_table()

    free_money = get_free_money_in_month()

    return render(
        request,
        "monthly.html",
        {
            "days": data,
            "daily_income": daily_income,
            "total_expenses": sum_of_usual_expenses,
            "year": year,
            "month": month,
            "monthes": MONTHES,
            "cur_month": MONTH_NAMES[month],
            "constant_expenses": sum_of_constant_expenses,
            "constant_incomes": sum_of_all_incomes,
            "free_money": free_money,
        },
    )


@login_required
def monthly_raw_expenses(request, year, month):

    data = UsualExpenses.get_objects_in_month(year, month)

    return render(
        request,
        "monthly_raw.html",
        {
            "expenses": data,
            "year": year,
            "month": month,
            "monthes": MONTHES,
            "cur_month": MONTH_NAMES[month],
        },
    )


def get_daily_income():

    monthly_income = get_free_money_in_month()
    num_of_days = abs((END_OF_MONTH - START_OF_MONTH).days + 1)
    daily_income = Decimal(monthly_income / num_of_days)

    return daily_income


def get_free_money_in_month():

    # Here will be model

    return Decimal(7000)


def get_balance_for_monthly_table():

    cur_day = START_OF_MONTH
    data = []
    accumulated = Decimal(0)
    daily_income = get_daily_income()
    accumulated_income = Decimal(0)
    accumulated_balance = Decimal(0)

    while cur_day != END_OF_MONTH + timedelta(1):
        spends_in_day = UsualExpenses.objects.filter(date=cur_day)
        accumulated_income += daily_income
        accumulated_balance += daily_income
        if len(spends_in_day) != 0:
            spends_list = []
            total_amount = Decimal(0)
            for spend in spends_in_day:
                spends_list.append(spend.category.name)
                total_amount += spend.amount
            accumulated += total_amount
            accumulated_balance -= total_amount
            data.append(
                {
                    "date": cur_day.date(),
                    "amount": total_amount,
                    "category": spends_list,
                    "accumulated_balance": accumulated_balance.quantize(
                        Decimal("1.00"), ROUND_FLOOR
                    ),
                }
            )
        else:
            data.append(
                {
                    "date": cur_day.date(),
                    "amount": Decimal(0).quantize(Decimal("1.00"), ROUND_FLOOR),
                    "category": ["No spends"],
                    "accumulated_balance": accumulated_balance.quantize(
                        Decimal("1.00"), ROUND_FLOOR
                    ),
                }
            )
        cur_day += timedelta(1)

    return data


def expenses_chart(request, year, month):

    last_day = monthrange(year, month)[1]

    START_OF_MONTH = datetime(year, month, 1)
    END_OF_MONTH = datetime(year, month, last_day)

    labels = []
    data = []

    for i in range(START_OF_MONTH.day, END_OF_MONTH.day + 1):
        labels.append(i)
        day = START_OF_MONTH + timedelta(i - 1)
        try:
            value = (
                UsualExpenses.objects.filter(date=day)
                .aggregate(Sum("amount"))["amount__sum"]
                .quantize(Decimal("1.00"), ROUND_FLOOR)
            )
            data.append(float(value))
        except AttributeError:
            data.append(None)

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        },
        status=200,
    )
