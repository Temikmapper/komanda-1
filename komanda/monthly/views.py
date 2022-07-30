from calendar import monthrange
from datetime import date, datetime, timedelta
from decimal import ROUND_FLOOR, Decimal

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random


from main.views import MONTH_NAMES, MONTHES
from expenses.models import UsualExpenses, ConstantExpenses
from incomes.models import AdditionalIncomes, ConstantIncomes
from monthly.models import FreeMoney
from monthly.forms import BumpFreeMoneyForm


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

    daily_income = get_daily_income(year, month).quantize(Decimal("1.00"), ROUND_FLOOR)
    sum_of_usual_expenses = UsualExpenses.get_sum_in_month(year, month)
    sum_of_all_incomes = ConstantIncomes.get_sum_in_month(
        year, month
    ) + AdditionalIncomes.get_sum_in_month(year, month)
    sum_of_constant_expenses = ConstantExpenses.get_sum_in_month(year, month)
    data = get_balance_for_monthly_table(year, month)

    free_money = FreeMoney.get_value(year, month)

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

@login_required
def bump_free_money(request, year, month):

    if request.method == "POST":
        form = BumpFreeMoneyForm(request.POST)
        if form.is_valid():
            free_money = form.save(commit=False)
            free_money.save()
        return redirect("redirect_to_view_month")
    else:
        form = BumpFreeMoneyForm()

    return render(
        request,
        "bump_free_money.html",
        {
            "form": form,
        },
    )


def get_daily_income(year, month):

    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    monthly_income = FreeMoney.get_value(year, month)
    num_of_days = abs((end_of_month - start_of_month).days + 1)
    daily_income = Decimal(monthly_income / num_of_days)

    return daily_income



def get_balance_for_monthly_table(year, month):

    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    cur_day = start_of_month
    data = []
    accumulated = Decimal(0)
    daily_income = get_daily_income(year, month)
    accumulated_income = Decimal(0)
    accumulated_balance = Decimal(0)

    while cur_day != end_of_month + timedelta(1):
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
                    "amount": None,
                    "category": ["No spends"],
                    "accumulated_balance": accumulated_balance.quantize(
                        Decimal("1.00"), ROUND_FLOOR
                    ),
                }
            )
        cur_day += timedelta(1)

    return data


def expenses_chart(request, year, month):

    monthly_table_data = get_balance_for_monthly_table(year, month)
    balance = [{'x': day['date'], 'y': day['accumulated_balance']} for day in monthly_table_data]
    expenses = [{'x': day['date'], 'y': day['amount']} for day in monthly_table_data]    
    
    categories_sum = {}
    expenses_list = UsualExpenses.get_objects_in_month(year, month)

    for expense in expenses_list:
        category = expense.category.name
        value = categories_sum.get(f'{category}', Decimal(0)) + expense.amount
        categories_sum.update({f'{category}': value})

    categories_labels = list(categories_sum.keys())
    categories_data = list(categories_sum.values())

    colors = []
    for category in categories_labels:
        color = [213, 38, 91]
        color_str = f'rgb({color[0]}, {color[1]}, {color[2]})'
        colors.append(color_str)

    return JsonResponse(
        data={
            "expenses": expenses,
            "balance": balance,
            "categories_labels": categories_labels,
            "categories_data": categories_data,
            "colors": colors,
        },
        status=200,
    )
