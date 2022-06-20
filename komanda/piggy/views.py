from django.shortcuts import render, redirect

from piggy.forms import PiggyAddForm, PiggyBumpForm, PiggyEditForm
from piggy.models import Piggies

# Create your views here.


def view_all_piggies(request):

    piggies = Piggies.objects.all()

    return render(
        request, "all_piggies.html", {"piggies": piggies}
    )


def view_piggy(request, id):

    piggy = Piggies.objects.get(id=id)

    return render(request, "view_piggy.html", {"piggy": piggy})


def piggy_add(request):

    if request.method == "POST":
        form = PiggyAddForm(request.POST)
        if form.is_valid():
            piggy = form.save(commit=False)
            piggy.save()
            return redirect("view_all_piggies")
    else:
        form = PiggyAddForm()

    return render(
        request,
        "add_piggy.html",
        {
            "form": form,
        },
    )


def piggy_delete(request, id):
    piggy = Piggies.objects.get(id=id)
    piggy.delete()

    return redirect("view_all_piggies")


def piggy_edit(request, id):

    piggy = Piggies.objects.get(id=id)

    if request.method == "POST":
        form = PiggyEditForm(request.POST)
        if form.is_valid():
            bump = form.save(commit=False)
            bump.value = piggy.get_current_value()
            bump.piggy = piggy
            bump.save()
            return redirect("view_all_piggies")
    else:
        form = PiggyEditForm()

    return render(
        request, "edit_piggy.html", {"form": form, "piggy": piggy}
    )


def piggy_bump(request, id):
    piggy = Piggies.objects.get(id=id)

    if request.method == "POST":
        form = PiggyBumpForm(request.POST)
        if form.is_valid():
            bump = form.save(commit=False)
            bump.piggy = piggy
            bump.percent = piggy.get_current_percent()
            bump.save()
            return redirect("view_all_piggies")
    else:
        form = PiggyBumpForm()

    return render(request, "bump_piggy.html", {"form": form})
