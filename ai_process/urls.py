from django.urls import path

from . import views

app_name = "ai_process"

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
]