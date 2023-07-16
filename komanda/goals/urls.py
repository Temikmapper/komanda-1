from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_all_goals, name="view_all_goals"),
    path("add", views.add_goal, name="add_goal"),
    path("<int:id>", views.view_goal, name="view_goal"),
    path("<int:id>/expenses", views.goal_expenses, name="goal_expenses"),
    path("<int:goal_id>/expenses/<int:goal_expense_id>/delete", views.delete_goal_expense, name="delete_goal_expense"),
    path("<int:id>/bumps", views.goal_bumps, name="goal_bumps"),
    path("<int:goal_id>/bumps/<int:goal_bump_id>/delete", views.delete_goal_bump, name="delete_goal_bump"),
    path("<int:id>/delete", views.delete_goal, name="delete_goal"),
    path("<int:id>/expense", views.add_expense_goal, name="expense_goal"),
    path("<int:id>/bump", views.bump_goal, name="bump_goal"),
    path("<int:id>/edit", views.edit_goal, name="edit_goal"),
]
