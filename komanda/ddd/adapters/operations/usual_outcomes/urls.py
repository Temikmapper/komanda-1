from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>", views.view_usual_outcome, name="ddd_view_usual_outcome"),
    path("add", views.add_outcome_form, name="ddd_add_outcome"),
    path("all", views.view_all_outcomes, name="ddd_all_outcomes"),
]
