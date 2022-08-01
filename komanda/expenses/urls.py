from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_monthly_expenses, name="view_monthly_expenses"),
    path("all", views.view_all_expenses, name="view_all_expenses"),
    path("add", views.add_usual_expense, name="add_expense"),
    path("add_constant", views.add_constant_expense, name="add_constant_expense"),
    path("delete/<int:id>", views.delete_expense, name="delete_expense"),
    path("categories", views.view_add_categories, name="view_add_categories"),
    path("categories/delete/<int:id>", views.delete_category, name="delete_category"),
    path(
        "constant/<int:id>/chart",
        views.chart,
        name="const_expenses_chart",
    ),
    path(
        "constant/<int:id>", views.view_constant_expense, name="view_constant_expense"
    ),
    path(
        "constant/<int:id>/edit",
        views.edit_constant_expense,
        name="edit_constant_expense",
    ),
    path(
        "constant/<int:id>/bump",
        views.bump_constant_expense,
        name="bump_constant_expense",
    ),
    path(
        "constant/all",
        views.view_all_constant_expenses,
        name="view_all_constant_expenses",
    ),
    path(
        "constant/<int:id>/delete",
        views.delete_constant_expense,
        name="delete_constant_expense",
    ),
]
