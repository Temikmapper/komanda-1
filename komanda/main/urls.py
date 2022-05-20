from django.urls import path, include

from . import views

from django.contrib.auth import views as views_auth

from goals import urls as goals_urls
from expenses import urls as expenses_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('test_base', views.test_base, name='test_base'),
    path('monthly/<int:year>/<int:month>', views.monthly, name='monthly'),
    path('monthly/<int:year>/<int:month>/raw', views.monthly_raw, name='monthly_raw'),
    path('monthly/<int:year>/<int:month>/income', views.monthly_income, name='monthly_income'),
    path('monthly/<int:year>/<int:month>/income/<int:id>/edit', views.income_edit, name='income_edit'),
    path('income/delete/<int:id>', views.income_delete, name='income_delete'),
    path('accounts/login/', views_auth.LoginView.as_view(next_page='/'), name='login'),
    path('accounts/logout/', views_auth.LogoutView.as_view(next_page='/'), name='logout'),
    path('goals/', include(goals_urls), name='view_all_goals'),
    path('expenses/', include(expenses_urls), name='view_all_expenses')
]