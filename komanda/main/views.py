from datetime import datetime, timedelta
from pydoc import describe
from unicodedata import category
from django.shortcuts import render, redirect
from main.models import Spendings, Categories
from main.forms import SpendForm, CategoryAddForm


def index(request):
    categories = Categories.objects.all()
    if request.method == "POST":
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
    else:
        form = CategoryAddForm()
    return render(request, 'index.html', {'form': form, 'categories': categories})
    

def test_base(request):
    return render(request, 'base.html')

def show_all(request):
    data = {'days': Spendings.objects.all()}
    return render(request, 'all.html', data)

def add_spend(request):
    if request.method == "POST":
        form = SpendForm(request.POST)
        if form.is_valid():
            spend = form.save(commit=False)
            spend.save()
    else:
        form = SpendForm()
    return render(request, 'add.html', {'form': form})

def delete_category(request, id):
    category = Categories.objects.get(id=id)
    category.delete()
    return redirect('index')