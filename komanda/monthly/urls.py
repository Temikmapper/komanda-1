from django.urls import path, include

from . import views
from incomes import urls as income_urls
from expenses import urls as expense_urls

urlpatterns = [
    path("", views.redirect_to_view_month, name="redirect_to_view_month"),
    path("<int:year>/<int:month>", views.view_month, name="view_month"),
    path(
        "<int:year>/<int:month>/raw", views.monthly_raw_expenses, name="view_month_raw"
    ),
    path(
        "<int:year>/<int:month>/expenses-chart",
        views.expenses_chart,
        name="expenses_chart",
    ),
    path(
        "<int:year>/<int:month>/incomes/",
        include(income_urls),
        name="view_monthly_incomes",
    ),
    path(
        "<int:year>/<int:month>/expenses/",
        include(expense_urls),
        name="view_monthly_expenses",
    ),
]
