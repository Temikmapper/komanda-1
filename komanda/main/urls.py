from django.urls import path, include

from . import views
from incomes import views as income_views

from django.contrib.auth import views as views_auth

from goals import urls as goals_urls
from expenses import urls as expenses_urls
from incomes import urls as income_urls
from monthly import urls as monthly_urls
from resume import urls as resume_urls
from piggy import urls as piggies_urls

urlpatterns = [
    path("", views.index, name="index"),
    path("test_base", views.test_base, name="test_base"),
    path("accounts/login/", views_auth.LoginView.as_view(next_page="/"), name="login"),
    path(
        "accounts/logout/", views_auth.LogoutView.as_view(next_page="/"), name="logout"
    ),
    path("goals/", include(goals_urls), name="view_all_goals"),
    path("expenses/", include(expenses_urls), name="view_all_expenses"),
    path("incomes/", include(income_urls), name="view_all_constant_incomes"),
    path("monthly/", include(monthly_urls), name="view_month"),
    path(
        "incomes/",
        income_views.view_all_constant_incomes,
        name="view_all_constant_incomes",
    ),
    path(
        "incomes/constant/all",
        income_views.view_all_constant_incomes,
        name="view_all_constant_incomes",
    ),
    path(
        "incomes/constant/add",
        income_views.add_constant_income,
        name="add_constant_income",
    ),
    path(
        "incomes/constant/delete/<int:id>",
        income_views.delete_constant_income,
        name="delete_constant_income",
    ),
    path(
        "incomes/constant/<int:id>",
        income_views.view_constant_income,
        name="view_constant_income",
    ),
    path("resume/", include(resume_urls), name="view_resume"),
    path("piggies/", include(piggies_urls), name="view_all_piggies"),
]
