from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_all_goals, name='view_all_goals'),
    path('add', views.add_goal, name='add_goal'),
    path('<int:id>/', views.view_goal, name='view_goal'),
    path('delete/<int:id>', views.delete_goal, name='delete_goal')
]