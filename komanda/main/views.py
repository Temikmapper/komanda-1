from datetime import datetime, timedelta
from django.shortcuts import render, redirect


def get_current_date():

    date = {
        "year": datetime.today().year,
        "month": datetime.today().month,
        "month_": str(datetime.today().month),
        "day_": str(datetime.today().day),
    }
    return date


CURRENT_DATE = get_current_date()
MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

jan = {"id": 1, "name": "January"}
feb = {"id": 2, "name": "February"}
mar = {"id": 3, "name": "March"}
apr = {"id": 4, "name": "April"}
may = {"id": 5, "name": "May"}
jun = {"id": 6, "name": "June"}
jul = {"id": 7, "name": "July"}
aug = {"id": 8, "name": "August"}
sep = {"id": 9, "name": "September"}
oct = {"id": 10, "name": "October"}
nov = {"id": 11, "name": "November"}
dec = {"id": 12, "name": "Decemeber"}
MONTHES = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]


def index(request):
    if request.user.is_authenticated:
        return redirect("/expenses/categories")
    else:
        return render(request, "index.html")


def test_base(request):
    return render(request, "base.html")
