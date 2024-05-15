from django.urls import path

from . import views

app_name = "explanations"

urlpatterns = [
    path("", views.index, name="index"),
]