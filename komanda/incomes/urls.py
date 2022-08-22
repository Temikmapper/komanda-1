from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_monthly_incomes, name="view_monthly_incomes"),
    path("add", views.add_income, name="income_add"),
    path("<int:id>/edit", views.edit_income, name="income_edit"),
    path("<int:id>/delete", views.income_delete, name="income_delete"),
    path("add_constant", views.add_constant_income, name="add_constant_income"),
    path("constant/<int:id>", views.view_constant_income, name="view_constant_income"),
    path(
        "constant/<int:id>/edit",
        views.edit_constant_income,
        name="edit_constant_income",
    ),
    path(
        "constant/<int:id>/bump",
        views.bump_constant_income,
        name="bump_constant_income",
    ),
    path(
        "constant/all",
        views.view_all_constant_incomes,
        name="view_all_constant_incomes",
    ),
    path(
        "constant/<int:id>/delete",
        views.delete_constant_income,
        name="delete_constant_income",
    ),
]
