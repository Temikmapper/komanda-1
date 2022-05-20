from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_monthly_incomes, name='view_monthly_incomes'),
    path('<int:id>/edit', views.income_edit, name='income_edit'),
    path('<int:id>/delete', views.income_delete, name='income_delete')
]