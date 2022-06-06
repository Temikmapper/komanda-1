from django.urls import path, include

from . import views

urlpatterns = [
    path('<int:year>/<int:month>', views.view_resume, name='view_resume'),
]