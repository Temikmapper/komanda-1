from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from main.views import CURRENT_DATE
from monthly.views import monthly_raw_expenses

from .models import Expenses, Categories
from .forms import AddExpenseForm, CategoryAddForm


@login_required
def view_all_expenses(request):
    data = Expenses.objects.all()
    return render(request, 'all_expenses.html', {'days': data, 'date': CURRENT_DATE})


@login_required
def view_add_categories(request):
    categories = Categories.objects.all()
    if request.method == "POST":
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
    else:
        form = CategoryAddForm()
    return render(request, 'categories.html', {'form': form, 'categories': categories, 'date': CURRENT_DATE})


@login_required
def delete_category(request, id):
    category = Categories.objects.get(id=id)
    category.delete()
    return view_add_categories(request)


@login_required
def add_expense(request):
    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            spend = form.save(commit=False)
            spend.save()
    else:
        form = AddExpenseForm()
    return render(request, 'add_expense.html', {'form': form, 'date': CURRENT_DATE})


@login_required
def delete_expense(request, id):
    expense = Expenses.objects.get(id=id)
    expense.delete()
    return redirect(request.GET['next'])
