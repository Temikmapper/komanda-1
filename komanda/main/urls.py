from django.urls import path, include

from . import views

from django.contrib.auth import views as views_auth

from goals import urls as goals_urls
from expenses import urls as expenses_urls
from monthly import urls as monthly_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('test_base', views.test_base, name='test_base'),
    path('accounts/login/', views_auth.LoginView.as_view(next_page='/'), name='login'),
    path('accounts/logout/', views_auth.LogoutView.as_view(next_page='/'), name='logout'),
    path('goals/', include(goals_urls), name='view_all_goals'),
    path('expenses/', include(expenses_urls), name='view_all_expenses'),
    path('monthly/', include(monthly_urls), name='view_month')
]