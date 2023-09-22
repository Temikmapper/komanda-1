from django.urls import path, include

from . import views
from incomes import views as income_views
from api import views as api_views

from django.contrib.auth import views as views_auth

from goals import urls as goals_urls
from expenses import urls as expenses_urls
from incomes import urls as income_urls
from monthly import urls as monthly_urls
from resume import urls as resume_urls
from piggy import urls as piggies_urls
from tableau import views as tableu_views
from ddd.adapters import urls as ddd_urls

from rest_framework import routers

router = routers.DefaultRouter()
router.register("usual_expenses", api_views.UsualExpensesViewSet)
router.register("categories", api_views.CategoriesViewSet)

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
    path("resume/", include(resume_urls), name="view_resume"),
    path("piggies/", include(piggies_urls), name="view_all_piggies"),
    path("api/", include(router.urls), name="api_root"),
    path("tableau/<int:year>", tableu_views.view_tableau, name="view_tableau"),
    path("ddd/", include(ddd_urls), name="ddd_urls"),
]
