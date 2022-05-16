from datetime import datetime, timedelta
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

def monthly(request, year, month):

    start_of_month = datetime(year, month, 1)
    end_of_month = datetime(year, month+1, 1) - timedelta(1)

    data = Spendings.objects.filter(date__gte=start_of_month).filter(date__lte=end_of_month).order_by('date')

    return render(request, 'monthly.html', {'date': CURRENT_DATE, 'days': data})