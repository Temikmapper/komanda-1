from audioop import reverse
from calendar import monthrange
from datetime import datetime, timedelta
from decimal import ROUND_05UP, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, Decimal
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from main.models import Spendings, Categories, Incomes
from main.forms import SpendForm, CategoryAddForm, IncomeEditForm, IncomeAddForm


def get_current_date():

    date = {'year': datetime.today().year,
            'month': datetime.today().month,
            'month_': str(datetime.today().month),
            'day_': str(datetime.today().day)}
    return date


CURRENT_DATE = get_current_date()
MONTH_NAMES = {1: 'January',
               2: 'February',
               3: 'March',
               4: 'April',
               5: 'May',
               6: 'June',
               7: 'July',
               8: 'August',
               9: 'September',
               10: 'October',
               11: 'November',
               12: 'December'}

jan = {'id': 1, 'name': 'January'}
feb = {'id': 2, 'name': 'February'}
mar = {'id': 3, 'name': 'March'}
apr = {'id': 4, 'name': 'April'}
may = {'id': 5, 'name': 'May'}
jun = {'id': 6, 'name': 'June'}
jul = {'id': 7, 'name': 'July'}
aug = {'id': 8, 'name': 'August'}
sep = {'id': 9, 'name': 'September'}
oct = {'id': 10, 'name': 'October'}
nov = {'id': 11, 'name': 'November'}
dec = {'id': 12, 'name': 'Decemeber'}
MONTHES = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]


def index(request):
    categories = Categories.objects.all()
    if request.method == "POST":
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
    else:
        form = CategoryAddForm()
    return render(request, 'index.html', {'form': form, 'categories': categories, 'date': CURRENT_DATE})


def test_base(request):
    return render(request, 'base.html')

@login_required
def show_all(request):
    data = Spendings.objects.all()
    return render(request, 'all.html', {'days': data, 'date': CURRENT_DATE})

@login_required
def add_spend(request):
    if request.method == "POST":
        form = SpendForm(request.POST)
        if form.is_valid():
            spend = form.save(commit=False)
            spend.save()
    else:
        form = SpendForm()
    return render(request, 'add.html', {'form': form, 'date': CURRENT_DATE})

@login_required
def delete_category(request, id):
    category = Categories.objects.get(id=id)
    category.delete()
    return redirect('index')

@login_required
def delete_expense(request, id, year, month):
    expense = Spendings.objects.get(id=id)
    expense.delete()
    return redirect('index')  # TODO редикрет обратно в raw

@login_required
def monthly(request, year, month):  # TODO рефакторить

    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    monthly_income = get_monthly_income(
        start_of_month).quantize(Decimal("1.00"), ROUND_FLOOR)
    daily_income = get_daily_income(start_of_month, end_of_month).quantize(
        Decimal("1.00"), ROUND_FLOOR)
    total_expenses = Spendings.objects.filter(date__gte=start_of_month).filter(
        date__lte=end_of_month).aggregate(Sum("amount"))['amount__sum']
    data = get_balance_for_monthly_table(start_of_month, end_of_month)

    return render(request, 'monthly.html',
                  {'date': CURRENT_DATE,
                   'days': data,
                   'daily_income': daily_income,
                   'monthly_income': monthly_income,
                   'total_expenses': total_expenses,
                   'year': year,
                   'month': month,
                   'monthes': MONTHES,
                   'cur_month': MONTH_NAMES[month]})

@login_required
def monthly_raw(request, year, month):

    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    data = Spendings.objects.filter(date__gte=start_of_month).filter(
        date__lte=end_of_month).order_by('date')

    return render(request, 'monthly_raw.html',
                  {'date': CURRENT_DATE,
                   'days': data,
                   'year': year,
                   'month': month,
                   'monthes': MONTHES,
                   'cur_month': MONTH_NAMES[month]})

@login_required
def monthly_income(request, year, month):
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
def income_edit(request, year, month, id):
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
def income_delete(request, id):
    income = Incomes.objects.get(id=id)
    income.delete()
    return redirect('index')


def get_monthly_income(date):
    total_monthly_income = Incomes.objects.filter(
        date=date).aggregate(Sum("value"))
    if total_monthly_income['value__sum'] == None:
        return Decimal(0.00)
    return total_monthly_income['value__sum']


def get_daily_income(start, finish):
    monthly_income = get_monthly_income(start)
    num_of_days = abs((finish-start).days+1)
    daily_income = Decimal(monthly_income/num_of_days)
    return daily_income


def get_balance_for_monthly_table(start_of_month, end_of_month):
    cur_day = start_of_month
    data = []
    accumulated = Decimal(0)
    daily_income = get_daily_income(start_of_month, end_of_month)
    accumulated_income = Decimal(0)
    accumulated_balance = Decimal(0)

    while (cur_day != end_of_month+timedelta(1)):
        spends_in_day = Spendings.objects.filter(date=cur_day)
        accumulated_income += daily_income
        accumulated_balance += daily_income
        if (len(spends_in_day) != 0):
            spends_list = []
            total_amount = Decimal(0)
            for spend in spends_in_day:
                spends_list.append(spend.category.name)
                total_amount += spend.amount
            accumulated += total_amount
            accumulated_balance -= total_amount
            data.append({'date': cur_day.date(),
                         'amount': total_amount,
                         'category': spends_list,
                         'accumulated_balance': accumulated_balance.quantize(Decimal("1.00"), ROUND_FLOOR)})
        else:
            data.append({'date': cur_day.date(),
                         'amount': Decimal(0).quantize(Decimal("1.00"), ROUND_FLOOR),
                         'category': ['No spends'],
                         'accumulated_balance': accumulated_balance.quantize(Decimal("1.00"), ROUND_FLOOR)})
        cur_day += timedelta(1)

    return data
