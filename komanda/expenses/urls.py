from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_all_expenses, name='view_all_expenses'),
    path('add', views.add_expense, name='add_expense'),
    path('delete/<int:id>', views.delete_expense, name='delete_expense'),
    path('categories', views.view_add_categories, name='view_add_categories'),
    path('categories/delete/<int:id>', views.delete_category, name='delete_category'),
    # path('<int:id>/', views.view_goal, name='view_goal'),
]