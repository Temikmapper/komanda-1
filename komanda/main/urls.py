from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_base', views.test_base, name='test_base'),
    path('all', views.show_all, name='show_all'),
    path('add', views.add_spend, name='add_spend'),
    path('delete/<int:id>', views.delete_category, name='delete_category'),
    path('monthly/<int:year>/<int:month>', views.monthly, name='monthly'),
    path('monthly/<int:year>/<int:month>/raw', views.monthly_raw, name='monthly_raw'),
]