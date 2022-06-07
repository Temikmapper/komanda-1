from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_all_piggies, name='view_all_piggies'),
    path('add', views.piggy_add, name='piggy_add'),
    path('<int:id>/edit', views.piggy_edit, name='piggy_edit'),
    path('<int:id>/delete', views.piggy_delete, name='piggy_delete'),
    path('<int:id>/bump', views.piggy_bump, name='piggy_bump')
]