from calendar import monthrange
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from main.models import Spendings, Categories
from main.forms import SpendForm, CategoryAddForm


def get_curent_date():

    date = {'year': datetime.today().year,
            'month': datetime.today().month}
    return date


CURRENT_DATE = get_curent_date()


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


def show_all(request):
    data = Spendings.objects.all()
    return render(request, 'all.html', {'days': data, 'date': CURRENT_DATE})


def add_spend(request):
    if request.method == "POST":
        form = SpendForm(request.POST)
        if form.is_valid():
            spend = form.save(commit=False)
            spend.save()
    else:
        form = SpendForm()
    return render(request, 'add.html', {'form': form, 'date': CURRENT_DATE})


def delete_category(request, id):
    category = Categories.objects.get(id=id)
    category.delete()
    return redirect('index')


def monthly(request, year, month): #TODO рефакторить
    month_names = {1: 'January',
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
    jan = {'id':1, 'name':'January'}
    feb = {'id':2, 'name':'February'}
    mar = {'id':3, 'name':'March'}
    apr = {'id':4, 'name':'April'}
    may = {'id':5, 'name':'May'}
    jun = {'id':6, 'name':'June'}
    jul = {'id':7, 'name':'July'}
    aug = {'id':8, 'name':'August'}
    sep = {'id':9, 'name':'September'}
    oct = {'id':10, 'name':'October'}
    nov = {'id':11, 'name':'November'}
    dec = {'id':12, 'name':'Decemeber'}
    monthes = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    # data = Spendings.objects.filter(date__gte=start_of_month).filter(
    #     date__lte=end_of_month).order_by('date')

    cur_day = start_of_month
    data = []
    while (cur_day != end_of_month+timedelta(1)):
        spends_in_day = Spendings.objects.filter(date=cur_day)
        if (len(spends_in_day) != 0):
            spends_list = []
            total_amount = Decimal(0)
            for spend in spends_in_day:
                spends_list.append(spend.category.name)
                total_amount+=spend.amount
            data.append({'date': cur_day.date(),'amount': total_amount, 'category': spends_list})
        else:
            data.append({'date': cur_day.date(), 'amount': Decimal(0), 'category': ['No spends']})
        cur_day+=timedelta(1)

    return render(request, 'monthly.html',
                  {'date': CURRENT_DATE,
                   'days': data,
                   'year': year,
                   'monthes': monthes,
                   'cur_month': month_names[month]})

def monthly_raw(request, year, month):
    month_names = {1: 'January',
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
    jan = {'id':1, 'name':'January'}
    feb = {'id':2, 'name':'February'}
    mar = {'id':3, 'name':'March'}
    apr = {'id':4, 'name':'April'}
    may = {'id':5, 'name':'May'}
    jun = {'id':6, 'name':'June'}
    jul = {'id':7, 'name':'July'}
    aug = {'id':8, 'name':'August'}
    sep = {'id':9, 'name':'September'}
    oct = {'id':10, 'name':'October'}
    nov = {'id':11, 'name':'November'}
    dec = {'id':12, 'name':'Decemeber'}
    monthes = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

    last_day = monthrange(year, month)[1]

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month, last_day)

    data = Spendings.objects.filter(date__gte=start_of_month).filter(
        date__lte=end_of_month).order_by('date')
    
    return render(request, 'monthly_raw.html',
                  {'date': CURRENT_DATE,
                   'days': data,
                   'year': year,
                   'monthes': monthes,
                   'cur_month': month_names[month]})
