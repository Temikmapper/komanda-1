from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.views import CURRENT_DATE

from .models import ConstantExpenses, ConstantExpenseHistory, Expenses, Categories
from .forms import AddExpenseForm, CategoryAddForm, ConstantExpenseAddForm, ConstantExpenseFinishForm, ExpenseEditForm


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


def view_expense(request, id):

    expense = ConstantExpenses.objects.get(id=id)

    latest_price = expense.amount

    return render(request, 'view_expense.html', {'date': CURRENT_DATE,
                                                 'expense': expense,
                                                 'latest_price': latest_price})


def add_constant_expense(request):

    if request.method == "POST":
        expense_form = ConstantExpenseAddForm(request.POST)
        value_form = ExpenseEditForm(request.POST)
        if expense_form.is_valid() and value_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.finish_date = expense.start_date + timedelta(760)
            expense.save()
            value = value_form.save(commit=False)
            expense = ConstantExpenses.objects.get(id=expense.id)
            value.date = datetime.today()
            value.expense = expense
            value.save()
    else:
        expense_form = ConstantExpenseAddForm()
        value_form = ExpenseEditForm()

    return render(request, 'add_const_expense.html', {'date': CURRENT_DATE,
                                                      'expense_form': expense_form,
                                                      'value_form': value_form})


def view_constant_expense(request, id):

    expense = ConstantExpenses.objects.get(id=id)
    expense_history = ConstantExpenseHistory.objects.filter(expense=expense)

    form = None

    if request.method == "POST":
        form = ExpenseEditForm(request.POST)
        finish_form = ConstantExpenseFinishForm(request.POST, instance=expense)
        if form.is_valid() and finish_form.is_valid():
            finish = finish_form.save(commit=False)
            finish.save()
            value = form.save(commit=False)
            value.date = datetime.today()
            value.expense = expense
            value.save()
    else:
        form = ExpenseEditForm()
        finish_form = ConstantExpenseFinishForm(instance=expense)

    return render(request, 'view_constant_expense.html', {'date': CURRENT_DATE,
                                                          'expense': expense,
                                                          'history': expense_history,
                                                          'form': form,
                                                          'finish_form': finish_form,
                                                          })


def view_all_constant_expenses(request):

    all_expenses = ConstantExpenses.objects.all()

    return render(request, 'view_all_constant_expenses.html', {'date': CURRENT_DATE,
                                                               'expenses': all_expenses})

def delete_constant_expense(request, id):
    expense = ConstantExpenses.objects.get(id=id)
    expense.delete()

    return view_all_constant_expenses(request)


@login_required
def delete_expense(request, id):
    expense = Expenses.objects.get(id=id)
    expense.delete()
    return view_all_expenses(request)
