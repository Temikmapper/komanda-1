from django.urls import path, include

from .operations.usual_outcomes import urls as usual_outcomes_urls

urlpatterns = [
    path("usual_outcomes/", include(usual_outcomes_urls), name="ddd_usual_outcomes"),
]