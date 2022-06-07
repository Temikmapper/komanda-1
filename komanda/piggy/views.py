from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, redirect

from main.views import CURRENT_DATE
from piggy.forms import PiggyAddForm, PiggyBumpForm
from piggy.models import Piggies

# Create your views here.


def view_all_piggies(request):
    piggies = Piggies.objects.all()

    return render(request, 'all_piggies.html', {'date': CURRENT_DATE,
                                                'piggies': piggies})


def piggy_add(request):

    if request.method == "POST":
        form = PiggyAddForm(request.POST)
        if form.is_valid():
            piggy = form.save(commit=False)
            piggy.save()
            return redirect('view_all_piggies')
    else:
        form = PiggyAddForm()

    return render(request, 'add_piggy.html', {'date': CURRENT_DATE,
                                              'form': form,
                                              })


def piggy_delete(request, id):
    piggy = Piggies.objects.get(id=id)
    piggy.delete()

    return view_all_piggies(request)


def piggy_edit(request, id):

    return render(request, 'edit_piggy.html', {'date': CURRENT_DATE})


def piggy_bump(request, id):
    piggy = Piggies.objects.get(id=id)

    if request.method == "POST":
        form = PiggyBumpForm(request.POST)
        if form.is_valid():
            bump = form.save(commit=False)
            bump.piggy = piggy
            bump.save()
            return view_all_piggies(request)
    else:
        form = PiggyBumpForm()

    return render(request, 'bump_piggy.html', {'date': CURRENT_DATE,
                                               'form': form})
