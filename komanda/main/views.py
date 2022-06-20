from datetime import datetime, timedelta
from django.shortcuts import render, redirect


MONTH_NAMES = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

jan = {"id": 1, "name": "Январь"}
feb = {"id": 2, "name": "Февраль"}
mar = {"id": 3, "name": "Март"}
apr = {"id": 4, "name": "Апрель"}
may = {"id": 5, "name": "Май"}
jun = {"id": 6, "name": "Июнь"}
jul = {"id": 7, "name": "Июль"}
aug = {"id": 8, "name": "Август"}
sep = {"id": 9, "name": "Сентябрь"}
oct = {"id": 10, "name": "Октябрь"}
nov = {"id": 11, "name": "Ноябрь"}
dec = {"id": 12, "name": "Декабрь"}

MONTHES = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]


def index(request):
    if request.user.is_authenticated:
        return redirect("/expenses/categories")
    else:
        return render(request, "index.html")


def test_base(request):
    return render(request, "base.html")
