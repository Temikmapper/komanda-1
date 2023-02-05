from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from incomes import models as income_models
from monthly import models as free_money_models
from expenses import models as expenses_models
from goals import models as goals_models

from main.views import MONTH_NAMES


def get_data_for_model(objects, year):
    item_categories = {}
    for item in objects:
        item_values = []
        for month_num in MONTH_NAMES.keys():
            item_values.append(item.get_value_in_month(year, month_num))
        item_values.append(sum(item_values))
        item_categories.update({item: item_values})

    items_total_list = list(item_categories.values())
    monthly_sum = []
    for i in range(13):
        sum_value = 0
        for item in range(len(item_categories.values())):
            sum_value += items_total_list[item][i]
        monthly_sum.append(sum_value)
    item_categories.update({"Итого": monthly_sum})
    return item_categories


def get_data_for_goals(objects, year):
    item_categories = {}
    for item in objects:
        item_values = []
        for month_num in MONTH_NAMES.keys():
            if item.date < date(year, month_num, 1):
                stats = {
                    "accumulated": 0,
                    "spent": 0,
                    "balance": 0,
                }
            else:
                stats = {
                    "accumulated": item.get_bumps_value_in_month(
                        year=year, month=month_num
                    ),
                    "spent": item.get_expenses_value_in_month(year=year, month=month_num),
                    "balance": item.get_balance_by_month(year=year, month=month_num),
                }
            item_values.append(stats)

        item_categories.update({item: item_values})

    items_total_list = list(item_categories.values())
    monthly_sum = []
    for i in range(12):
        sum_value = 0
        for item in range(len(item_categories.values())):
            print(items_total_list[item][i])
            sum_value += items_total_list[item][i]["accumulated"]
        monthly_sum.append({"accumulated": sum_value})
    item_categories.update({"Итого": monthly_sum})
    return item_categories


@login_required
def view_tableau(request, year):
    regular_incomes = income_models.ConstantIncomes.objects.filter(
        start_date__lte=date(year, 1, 1)
    ).filter(finish_date__gte=date(year, 12, 31))
    income_categories = get_data_for_model(regular_incomes, year)

    free_money = free_money_models.FreeMoney.objects.first()
    free_money_values = []
    for month_num in MONTH_NAMES.keys():
        free_money_values.append(free_money.get_value(year, month_num))
    free_money_values.append(sum(free_money_values))

    balance_after_free_money = [
        i - fm for i, fm in zip(income_categories["Итого"], free_money_values)
    ]

    regular_expenses = expenses_models.ConstantExpenses.objects.filter(
        start_date__lte=date(year, 12, 31)
    ).filter(finish_date__gte=date(year, 1, 1))
    expenses_categories = get_data_for_model(regular_expenses, year)

    balance_after_regular_expenses = [
        fm - e for fm, e in zip(balance_after_free_money, expenses_categories["Итого"])
    ]

    goals = goals_models.Goals.objects.filter(date__gte=date(year, 1, 1))
    goals_categories = get_data_for_goals(goals, year)

    balance_after_goals = [
        e - g["accumulated"]
        for e, g in zip(balance_after_regular_expenses, goals_categories["Итого"])
    ]

    return render(
        request,
        "tableau.html",
        {
            "year": year,
            "monthes": MONTH_NAMES,
            "income_categories": income_categories,
            "free_money_per_month": free_money_values,
            "balance_after_free_money": balance_after_free_money,
            "expenses_categories": expenses_categories,
            "balance_after_regular_expenses": balance_after_regular_expenses,
            "goals_categories": goals_categories,
            "balance_after_regular_goals": balance_after_goals,
        },
    )
