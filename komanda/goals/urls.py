from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_all_goals, name="view_all_goals"),
    path("add", views.add_goal, name="add_goal"),
    path("<int:id>", views.view_goal, name="view_goal"),
    path("<int:id>/delete", views.delete_goal, name="delete_goal"),
    path("<int:id>/expense", views.add_expense_goal, name="expense_goal"),
    path("<int:id>/bump", views.bump_goal, name="bump_goal"),
    path("<int:id>/edit", views.edit_goal, name="edit_goal"),
]
